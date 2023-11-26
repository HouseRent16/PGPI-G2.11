#Create enumerate file

from enum import Enum

class Category(Enum):

    HOUSE = 'Casa'
    APARTMENT = 'Apartamento'
    PENTHOUSE = 'Ático'
    DUPLEX = 'Dúplex'
    CHALET = 'Chalet'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
class Request(Enum):

    NOT_REQUESTED = 'Sin solicitar'
    PENDING = 'Pendiente'
    ACCEPTED = 'Aceptada'
    DENIED = 'Denegada'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class PaymentMethod(Enum):

    ONLINE = 'ONLINE'
    CASH = 'EFECTIVO'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
class Gender(Enum):

    MALE = 'Masculino'
    FEMALE = 'Femenino'
    OTHER = 'Otro'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class ClaimStatus(Enum):

    PENDING = 'Pendiente'
    RESOLVED = 'Resuelta'
    REJECTED = 'Rechazada'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

# choices=[('Pending', 'Pendiente'), ('Confirmed', 'Confirmada'), ('Cancelled', 'Cancelada')
class BookingStatus(Enum):
    
        PENDING = 'Pendiente'
        CONFIRMED = 'Confirmada'
        CANCELLED = 'Cancelada'
    
        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)
        
class Service(Enum):

    WIFI = 'Wifi'
    WASHING_MACHINE = 'Lavadora'
    AIR_CONDITIONING = 'Aire acondicionado'
    HAIRDRYER = 'Secador de pelo'
    KITCHEN = 'Cocina'
    HEATER = 'Calefacción'
    TV = 'Televisión'
    IRON = 'Plancha'
    FREE_PARKING = 'Parking gratuito'
    LAUNDRY_SERVICE = 'Servicio de Lavandería'
    HOUR_RECEPTION_24H = 'Recepción 24h'
    BREAKFAST_INCLUDED = 'Desayuno incluido'
    SWIMMING_POOL = 'Piscina'
    JACUZZI = 'Jacuzzi'
    BARBECUE = 'Barbacoa'
    GYM = 'Gimnasio'
    PETS_ALLOWED = 'Mascotas permitidas'
    ACCESSIBILITY = 'Accesibilidad'
    SMOKING_AREA = 'Zona de fumadores'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
