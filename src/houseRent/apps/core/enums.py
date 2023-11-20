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

class PaymentMethod(Enum):

    ONLINE = 'ONLINE'
    EFECTIVO = 'EFECTIVO'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
