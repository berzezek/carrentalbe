# Generated by Django 5.1.3 on 2024-11-26 10:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(choices=[('audi', 'Audi'), ('bmw', 'BMW'), ('chevrolet', 'Chevrolet'), ('citroen', 'Citroen'), ('fiat', 'Fiat'), ('ford', 'Ford'), ('honda', 'Honda'), ('hyundai', 'Hyundai'), ('kia', 'Kia'), ('mazda', 'Mazda'), ('mercedes', 'Mercedes'), ('nissan', 'Nissan'), ('opel', 'Opel'), ('peugeot', 'Peugeot'), ('renault', 'Renault'), ('seat', 'Seat'), ('skoda', 'Skoda'), ('suzuki', 'Suzuki'), ('toyota', 'Toyota'), ('volkswagen', 'Volkswagen'), ('volvo', 'Volvo')], max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('body_type', models.CharField(choices=[('sedan', 'Sedan'), ('hatchback', 'Hatchback'), ('station_wagon', 'Station Wagon'), ('suv', 'SUV'), ('minivan', 'Minivan'), ('convertible', 'Convertible'), ('coupe', 'Coupe'), ('pickup', 'Pickup')], max_length=50)),
                ('options', models.JSONField(blank=True, default=list, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('passport', models.CharField(blank=True, max_length=50, null=True)),
                ('driver_license', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='drivers/%Y/%m/%d')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('new', 'New'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='new', max_length=10)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='rental.driver')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='rental.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='rental.vehiclecategory'),
        ),
        migrations.CreateModel(
            name='VehiclePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_photo', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/%Y/%m/%d')),
                ('photo_date', models.DateTimeField(auto_now_add=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rental.vehicle')),
            ],
        ),
    ]