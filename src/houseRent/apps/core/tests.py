from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Address, Accommodation
import datetime

class AccommodationTestCase(TestCase):
    def setUp(self):
        # Crear una dirección
        self.address = Address.objects.create(
            unit_number='1',
            street_number='1',
            address_line_1='Calle Ejemplo',
            address_line_2='Piso Ejemplo',
            city='Ciudad Ejemplo',
            region='Región Ejemplo',
            country='ES',
            postal_code='12345'
        )

        # Crear un usuario (propietario)
        CustomUser = get_user_model()
        self.owner = CustomUser.objects.create_user(
            username='usuario_ejemplo',
            password='contraseña_ejemplo',
            first_name='Nombre Ejemplo',
            last_name='Apellido Ejemplo',
            birth_date=datetime.date(2000, 1, 1),
            phone='123456789',
            address=self.address,
            email='usuario@ejemplo.com',
            dni='12345678A',
            gender='MALE',
            request='NOT_REQUESTED'
        )

        # Crear un alojamiento
        self.accommodation = Accommodation.objects.create(
            owner=self.owner,
            name='Nombre Ejemplo',
            description='Descripción Ejemplo',
            address=self.address,
            category='HOUSE',
            capacity=1,
            price=1.0
        )

    def test_accommodation_str(self):
        # Comprobar que el método __str__ funciona como se espera
        self.assertEqual(str(self.accommodation), f"{self.accommodation.name} - {self.address.unit_number}, {self.address.street_number}, {self.address.address_line_1}, {self.address.address_line_2}, {self.address.city}, {self.address.region}, {self.address.country.name}")