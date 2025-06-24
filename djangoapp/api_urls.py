from rest_framework.routers import DefaultRouter
from django.urls import path, include
# from .views import CarModelViewSet  # Temporarily disabled

router = DefaultRouter()
# router.register(r'cars', CarModelViewSet)  # Temporarily disabled

urlpatterns = [
    path('', include(router.urls)),
]