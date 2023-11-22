from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from .enums import Category,PaymentMethod
from django_countries.fields import CountryField

class Address(models.Model):
    unit_number = models.CharField(max_length=10, blank=True, null=True)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=200)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    country = CountryField()

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['region']),
            models.Index(fields=['postal_code'])
        ]

    def __str__(self):
        parts = [self.unit_number, self.street_number, self.address_line_1, self.address_line_2, self.city, self.region, self.postal_code]
        return ", ".join(filter(None, parts))


class CustomUser(AbstractUser):
    birthDate = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=9, blank=True, null=True)
    email = models.EmailField(unique=True)
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

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return f"{self.accommodation.name} : {self.title}"


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
        return f"{self.client.username} : {self.accommodation.name} - {self.date}"


class Book(models.Model):
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    paymentMethod=models.CharField(max_length=10, choices=PaymentMethod.choices())
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amountPeople=models.IntegerField()
    isActive=models.BooleanField()
    accommodation=models.ForeignKey(Accommodation,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
    
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('La fecha de inicio no puede ser mayor que la fecha de fin')
        if self.amountPeople < 1:
            raise ValidationError('El número de personas no puede ser menor que 1')
    
    def __str__(self):
        return f"{self.user.username} : {self.accommodation.name} - {self.start_date} - {self.end_date}"
