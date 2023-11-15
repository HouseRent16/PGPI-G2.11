from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Address, Accommodation
import datetime

class AccommodationTestCase(TestCase):
    def setUp(self):
        # Crear una dirección
        self.address = Address.objects.create(
            street="Calle Ejemplo",
            city="Ciudad Ejemplo",
            province="Provincia Ejemplo",
            zipcode="12345",
            number="10",
            country="País Ejemplo"
        )

        # Crear un usuario (propietario)
        CustomUser = get_user_model()
        self.owner = CustomUser.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123',
            birthDate=datetime.date(1990, 1, 1),
            phone='123456789',
            address=self.address,
            dni='12345678Z',
            gender='M',
            isOwner=True
        )

        # Crear un alojamiento
        self.accommodation = Accommodation.objects.create(
            name="Alojamiento Ejemplo",
            description="Descripción Ejemplo",
            owner=self.owner,
            price=100.00,
            address=self.address,
            category="Categoría Ejemplo"
        )

    def test_accommodation_str(self):
        # Comprobar que el método __str__ funciona como se espera
        self.assertEqual(str(self.accommodation), f"{self.accommodation.name} - {self.address.street} {self.address.number}, {self.address.city}, {self.address.province}, {self.address.country}")