from rest_framework import viewsets

from rental.models import VehiclePhoto, VehicleCategory, Vehicle, Driver, Order
from .serializers import VehiclePhotoSerializer, VehicleCategorySerializer, VehicleSerializer, DriverSerializer, OrderSerializer


class VehiclePhotoViewSet(viewsets.ModelViewSet):
    queryset = VehiclePhoto.objects.all()
    serializer_class = VehiclePhotoSerializer


class VehicleCategoryViewSet(viewsets.ModelViewSet):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
