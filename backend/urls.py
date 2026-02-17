from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, RegisterView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
