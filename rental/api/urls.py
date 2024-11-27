from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vehicle-photos', views.VehiclePhotoViewSet)
router.register(r'vehicle-categories', views.VehicleCategoryViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = router.urls