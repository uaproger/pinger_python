from django.views.generic import ListView
from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Service.objects.all()
        return Service.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def ping(self, request, pk=None):
        service = self.get_object()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }

        try:
            response = requests.get(service.url, timeout=10, headers=headers, allow_redirects=True)
            service.status_code = response.status_code

            service.is_online = (200 <= response.status_code < 400)
        except Exception as e:
            service.status_code = 0
            service.is_online = False
            print(f"Error pinging {service.url}: {e}")

        service.save()
        return Response({
            'status': 'ok',
            'is_online': service.is_online,
            'status_code': service.status_code
        })


class BaseMonitorView(ListView):
    model = Service
    context_object_name = 'services'


class DashboardView(BaseMonitorView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Статус сервісів"
        return context


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
