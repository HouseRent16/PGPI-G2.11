from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.
class Address(models.Model):
    street = models.TextField()
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    code = models.CharField(max_length=10, 
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Introduzca un código postal válido',
                code='invalid_chart_field'
            ),
        ])
    number = models.CharField(max_length=10, 
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Introduzca un número válido',
                code='invalid_chart_field'
            )
        ])
    country = models.CharField(max_length=100)

class CustomUser(AbstractUser, PermissionsMixin):
    birthDate = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=9, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    dni = models.CharField(max_length=9, 
        validators=[
            RegexValidator(
                regex='^\d{8}[a-zA-Z]$',
                message='Introducza un DNI válido',
                code='invalid_chart_field'
                )
            ])
    gender = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    isOwner = models.BooleanField(default=False)

class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

class Meta:
    app_label = "houseRent"
    verbose_name = "User"
    verbose_name_plural = "Users"