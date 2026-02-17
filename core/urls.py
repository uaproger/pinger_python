from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from pinger_app.views import ServiceViewSet, DashboardView


router = DefaultRouter()
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pinger_app.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', DashboardView.as_view(), name='dashboard'),
]
