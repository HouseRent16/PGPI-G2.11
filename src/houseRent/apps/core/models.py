from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
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

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}, {self.province}, {self.country}"


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
        return f"{self.username}"
      
      
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=544)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.name} - {self.description}"



class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024,blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=Category.choices())
    service = models.ManyToManyField(Service)

    class Meta:
        verbose_name = "Alojamiento"
        verbose_name_plural = "Alojamientos"

    def clean(self):
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

    def __str__(self):

        return f"{self.name} - {str(self.address)}"
    
class Image(models.Model):
    title = models.TextField(max_length=100,blank=True, null=True)
    description = models.TextField(max_length=1024,blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="images/")
    alt = models.CharField(max_length=200)
    publicationDate = models.DateField(auto_now=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return f"{self.accommodation} - {self.alt}"    
    
    class Comment(models.Model):
        title = models.TextField(max_length=100,blank=True, null=True)
        description = models.TextField(max_length=1024,blank=True, null=True)
        publicationDate = models.DateField(auto_now_add=True)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])
        accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)



class Claim(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=1024,blank=True, null=True)
    publicationDate = models.DateField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reclamación"
        verbose_name_plural = "Reclamaciones"

    def __str__(self):
        return f"{self.accommodation.name} : {self.title}"



class Favorite(models.Model):
    date = models.DateField(auto_now=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return f"{self.client.name} : {self.accommodation.name} - {self.date}"


class Book(models.Model):
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    paymentMethod=models.TextChoices("Cobro en la entrega","Pago Online")
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amountPeople=models.IntegerField()
    price=models.DecimalField(decimal_places=2, max_digits=10)
    isActive=models.BooleanField()
    accommodation=models.ForeignKey(Accommodation,on_delete=models.CASCADE)
