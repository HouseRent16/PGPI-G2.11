from django import forms
from apps.core.models  import Book, CustomUser
from utils.validators import Validators
from django.db.models import Q
import datetime
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



class BookingRequest(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
    class Meta:
        model=Book
        fields=['start_date','end_date','payment_method','amount_people','special_requests', 'accommodation']

        widgets = {
            'accommodation': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'required': False})
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
        Validators.validate_future_datetime(start_date)
        return start_date
    
    def clean_amount_people(self):
         amount_people = self.cleaned_data['amount_people']
         if amount_people < 1:
              raise forms.ValidationError('El número de personas debe ser mayor a 0')
         return amount_people
    
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')  # Usa get() para evitar KeyError
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
                raise forms.ValidationError('La fecha de fin debe ser posterior a la de inicio')
        Validators.validate_future_datetime(end_date)
        return end_date
    
    def clean_accommodation(self):
        accommodation = self.cleaned_data.get('accommodation')
        start_date = self.cleaned_data.get('start_date') 
        end_date = self.cleaned_data.get('end_date')
        amount_people = self.cleaned_data['amount_people']
        if accommodation and accommodation.capacity < amount_people:
                    self.add_error('amount_people', 'Se ha superado la capacidad máxima')
        if start_date and end_date and accommodation:
            overlapping_booking = Book.objects.filter(
                  Q(accommodation=accommodation) &
                  (Q(end_date__gt=start_date, start_date__lt=end_date) | Q(end_date__lt=end_date, end_date__gt=start_date) | Q(start_date__gt=start_date, start_date__lt=end_date))
            ).exclude(is_active=False)
            if overlapping_booking.exists():
                self.add_error('end_date', 'No hay disponibilidad del alojamiento seleccionado en las fechas especificadas.')
        
        
        return accommodation

    def clean_amount_people(self):
        cleaned_data = super().clean()
        amount_people = self.cleaned_data['amount_people']
        accommodation = cleaned_data.get('accommodation')
        if accommodation and accommodation.capacity < amount_people:
            raise forms.ValidationError('Se ha superado la capacidad máxima')
        return amount_people
                                                                        
class UserBookRequest(forms.ModelForm):
    phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control'}, initial='ES',)
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'phone', 'dni', 'gender']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Número de teléfono',
            'birth_date': 'Fecha de nacimiento',
            'dni': 'DNI',
            'gender': 'Género',
        }
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        id = self.instance.id if self.instance else None
        exist_user = CustomUser.objects.filter(email=email).exclude(id=id).exists()
        if(exist_user):
            raise forms.ValidationError('Ya existe dicho correo. Si tiene una cuenta inicie sesión, en caso contrario ingrese uno válido.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        id = self.instance.id if self.instance else None
        exist_user = CustomUser.objects.filter(phone=phone).exclude(id=id).exists()
        if(exist_user):
            raise forms.ValidationError('Ya existe dicho teléfono. Si tiene una cuenta inicie sesión, en caso contrario ingrese uno válido.')
        return phone
    
    def clean_dni(self):
        id = self.instance.id if self.instance else None
        dni = self.cleaned_data.get('dni')
        exist_user = CustomUser.objects.filter(dni=dni).exclude(id=id).exists()
        if(exist_user):
            raise forms.ValidationError('Ya existe dicho dni. Si tiene una cuenta inicie sesión, en caso contrario ingrese uno válido.')
        return dni
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        current_date = datetime.date.today()
        years = (current_date - birth_date) 
        years = years.days / 365
        if years < 18:
             raise forms.ValidationError('Debe ser mayor de edad')
        return birth_date