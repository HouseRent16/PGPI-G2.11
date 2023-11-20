from django.core.exceptions import ValidationError
from django.utils import timezone


class Validators:
    @staticmethod
    def validate_future_datetime(value):
        if value <= timezone.now():
            raise ValidationError('The minimum date is today')
        
    @staticmethod
    def validate_dates(init_date, end_date):
            if init_date and end_date and init_date > end_date:
                raise ValidationError('The start date must be before the end date')