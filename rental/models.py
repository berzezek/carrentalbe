from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image


class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='photos')
    original_photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d', blank=True, null=True)
    photo_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.original_photo and not self.thumbnail:
            image = Image.open(self.original_photo)
            
            # Настройки размеров
            target_width, target_height = 1060, 1060

            # Определяем пропорции оригинального изображения
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            target_aspect_ratio = target_width / target_height

            # Сохраняем пропорции или обрезаем
            if aspect_ratio > target_aspect_ratio:
                # Изображение шире целевого размера — обрезаем по ширине
                new_height = target_height
                new_width = int(target_height * aspect_ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                left = (new_width - target_width) // 2
                image = image.crop((left, 0, left + target_width, target_height))
            elif aspect_ratio < target_aspect_ratio:
                # Изображение выше целевого размера — обрезаем по высоте
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                top = (new_height - target_height) // 2
                image = image.crop((0, top, target_width, top + target_height))
            else:
                # Пропорции совпадают — просто изменяем размер
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # Создаём и сохраняем миниатюру
            temp_thumb = BytesIO()
            image.save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)

            self.thumbnail.save(f"thumb_{self.original_photo.name}", ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo of {self.vehicle.id}. {self.vehicle.brand} - {self.vehicle.model}"


class VehicleCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Vehicle(models.Model):
    VEHICLE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('station_wagon', 'Station Wagon'),
        ('suv', 'SUV'),
        ('minivan', 'Minivan'),
        ('convertible', 'Convertible'),
        ('coupe', 'Coupe'),
        ('pickup', 'Pickup'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('AT', 'Automatic Transmission'),
        ('MT', 'Manual Transmission'),
    ]

    ENGINE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    BRAND_CHOICES = [
        ('audi', 'Audi'),
        ('bmw', 'BMW'),
        ('chevrolet', 'Chevrolet'),
        ('citroen', 'Citroen'),
        ('fiat', 'Fiat'),
        ('ford', 'Ford'),
        ('honda', 'Honda'),
        ('hyundai', 'Hyundai'),
        ('kia', 'Kia'),
        ('mazda', 'Mazda'),
        ('mercedes', 'Mercedes'),
        ('nissan', 'Nissan'),
        ('opel', 'Opel'),
        ('peugeot', 'Peugeot'),
        ('renault', 'Renault'),
        ('seat', 'Seat'),
        ('skoda', 'Skoda'),
        ('suzuki', 'Suzuki'),
        ('toyota', 'Toyota'),
        ('volkswagen', 'Volkswagen'),
        ('volvo', 'Volvo'),
    ]

    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name='vehicles')  
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES)
    options = models.JSONField(default=list, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=VEHICLE_STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.id}.{self.brand} - {self.model}"


class Driver(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True, null=True)
    passport = models.CharField(max_length=50, blank=True, null=True)
    driver_license = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='drivers/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return f"{self.driver_license} {self.first_name} {self.last_name}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='orders')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Order {self.id}. {self.vehicle} - {self.driver}"