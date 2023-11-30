from django.core.exceptions import ValidationError
from django.utils import timezone


class Validators:
    @staticmethod
    def validate_future_datetime(value):
        if value and value < timezone.now():
            raise ValidationError('La fecha mínima es la actual')
        
    @staticmethod
    def validate_dates(init_date, end_date):
            if init_date and end_date and init_date > end_date:
                raise ValidationError('La fecha de fin debe ser posterior a la de inicio')