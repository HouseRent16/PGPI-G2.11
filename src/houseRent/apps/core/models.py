from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from .enums import Category

class Address(models.Model):
    street = models.TextField()
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10, 
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

class CustomUser(AbstractUser):
    birthDate = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=9, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
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

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        return f"{self.street} {self.number}, {self.city}, {self.province}, {self.country}"

class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=Category.choices())

    class Meta:
        verbose_name = "Alojamiento"
        verbose_name_plural = "Alojamientos"

    def clean(self):
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

    def __str__(self):
        return f"{self.name} - {self.address}"
    
class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    alt = models.CharField(max_length=200)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return f"{self.accommodation} - {self.alt}"

