from django import forms
from apps.core.models  import Book
from utils.validators import Validators
from django.utils import timezone 


class BookingRequest(forms.ModelForm):
    class Meta:
        model=Book
        fields=['start_date','end_date','payment_method','amount_people','special_requests']

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control'})
        }

        labels = {
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de finalización',
            'payment_method': 'Método de pago',
            'amount_people': 'Número de personas',
            'special_requests': 'Notas especiales'
        }

        
    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        print('entra')
        print(start_date)
        #Validators.validate_future_datetime(start_date)
        return start_date
    
    def clean_amount_people(self):
         amount_people = self.cleaned_data['amount_people']
         if amount_people < 1:
              raise forms.ValidationError('El número de personas debe ser mayor a 0')
         return amount_people
    
    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        print('entra')
        print(start_date, end_date)
        if start_date and end_date and start_date > end_date:
                print('error')
                raise forms.ValidationError('La fecha de fin debe ser posterior a la de inicio')
        Validators.validate_future_datetime(end_date)
        Validators.validate_dates(start_date, end_date)

        return end_date