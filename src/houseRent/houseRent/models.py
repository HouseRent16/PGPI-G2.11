from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

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

class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, min_value=1)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class CustomUser(AbstractUser):
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
    