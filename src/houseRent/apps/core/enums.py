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