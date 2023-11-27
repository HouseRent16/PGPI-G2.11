from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.forms import ValidationError
from .enums import Gender, Request, Category, PaymentMethod, ClaimStatus, BookingStatus
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Address(models.Model):
    # Es el número asignado a un edificio a lo largo de una calle o una vía
    street_number = models.CharField(max_length=8, blank=False, null=False)
    # Contiene la parte principal de la dirección, como el nombre de la calle o de la vía
    address_line = models.TextField(blank=False, null=False)
    city = models.CharField(max_length=256, blank=False, null=False)
    region = models.CharField(max_length=256, blank=False, null=False)
    country = CountryField(blank_label='(seleccionar país)', blank=False, null=False)
    postal_code = models.CharField(max_length=16, blank=False, null=False)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['region']),
            models.Index(fields=['postal_code'])
        ]

    def __str__(self):
        parts = [self.street_number, self.address_line, self.city, self.region, self.country.name]
        return ", ".join(filter(None, parts))


class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=False, null=False)
    phone = PhoneNumberField(blank=False, null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False)
    dni = models.CharField(
        max_length=9, 
        unique=True, 
        blank=False, 
        null=False, 
        validators=[
            RegexValidator(
                regex='^\d{8}[a-zA-Z]$',
                message='Introducza un DNI válido',
                code='invalid_dni'
                )
            ])
    gender = models.CharField(max_length=16, choices=Gender.choices(), blank=False, null=False)
    request = models.CharField(max_length=16, choices=Request.choices(), default=Request.NOT_REQUESTED)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        indexes = [
            models.Index(fields=['dni']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.username}"
    
class Service(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name}"

class Accommodation(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(max_length=1024, blank=False, null=False)
    capacity = models.PositiveIntegerField(blank=False, null=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=8, blank=False, null=False, validators=[MinValueValidator(0)], help_text='Ingresa un valor positivo')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False)
    category = models.CharField(max_length=16, choices=Category.choices(), blank=False, null=False)
    service = models.ManyToManyField(Service, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=False, null=False)
    modification_date = models.DateField(auto_now=True, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        verbose_name = "Alojamiento"
        verbose_name_plural = "Alojamientos"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner']),
            models.Index(fields=['category']),
        ]

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

    def __str__(self):
        return f"{self.name} - {str(self.address)}"
    
class Image(models.Model):
    title = models.TextField(max_length=64, blank=False, null=False)
    description = models.TextField(max_length=1024)
    order = models.PositiveIntegerField(blank=False, null=False)
    image = models.ImageField(
        upload_to="images/",
        blank=False,
        null=False,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])
        ]
    )
    alt = models.CharField(max_length=256, blank=False, null=False)
    publication_date = models.DateField(auto_now=True, blank=False, null=False)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"
        unique_together = ('accommodation', 'order')

    def __str__(self):
        return f"{self.accommodation} - {self.alt}"    
    
class Comment(models.Model):
    title = models.TextField(max_length=64, blank=False, null=False)
    description = models.TextField(max_length=1024)
    publication_date = models.DateField(auto_now_add=True, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], blank=False, null=False)
    response = models.TextField(max_length=1024)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['accommodation']),
        ]

    def __str__(self):
        return f"{self.accommodation.name} : {self.title}"


class Claim(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False, null=False)
    publication_date = models.DateField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=16, choices=ClaimStatus.choices(), default=ClaimStatus.PENDING, blank=False, null=False)
    response = models.TextField(max_length=1024)

    class Meta:
        verbose_name = "Reclamación"
        verbose_name_plural = "Reclamaciones"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['accommodation']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.accommodation.name} : {self.title}"

class Favorite(models.Model):
    date = models.DateField(auto_now=True, blank=False, null=False)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        unique_together = ('accommodation', 'user')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['accommodation']),
        ]

    def __str__(self):
        return f"{self.user.username} : {self.accommodation.name} - {self.date}"

class Book(models.Model):
    start_date=models.DateTimeField(blank=False, null=False)
    end_date=models.DateTimeField(blank=False, null=False)
    payment_method=models.CharField(max_length=16, choices=PaymentMethod.choices(), blank=False, null=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    amount_people=models.PositiveIntegerField(blank=False, null=False)
    is_active=models.BooleanField()
    accommodation=models.ForeignKey(Accommodation,on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=16, choices=BookingStatus.choices(), default=BookingStatus.PENDING, blank=False, null=False)
    special_requests = models.TextField()

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['accommodation']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError('La fecha de inicio no puede ser mayor que la fecha de fin')
        if self.amountPeople < 1:
            raise ValidationError('El número de personas no puede ser menor que 1')
        
        overlapping_bookings = Book.objects.filter(
            accommodation=self.accommodation,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk)  # Excluye la reserva actual en caso de que se esté editando

        if overlapping_bookings.exists():
            raise ValidationError('El alojamiento no está disponible para las fechas seleccionadas')
    
    def __str__(self):
        return f"{self.user.username} : {self.accommodation.name} - {self.start_date} - {self.end_date}"
