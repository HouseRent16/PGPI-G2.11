from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from apps.core.models import Accommodation, CustomUser, Address, Service
from django.contrib.auth.forms import AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterUser(forms.ModelForm):
    phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control'}, initial='ES')
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'phone', 'password', 'dni', 'gender']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Número de teléfono',
            'birth_date': 'Fecha de nacimiento',
            'dni': 'DNI',
            'gender': 'Género',
        }

        help_texts = {
            'username': None,
            'email': None,
            'password': None,
            'first_name': None,
            'last_name': None,
            'phone': None,
            'birth_date': None,
            'dni': None,
            'gender': None,
        }

        error_messages = {
            'username': {
                'unique': 'Ya existe un usuario con ese nombre de usuario'
            },
            'email': {
                'unique': 'Ya existe un usuario con ese correo electrónico'
            }
        }

        validators = {
            'username': [
                RegexValidator(
                    regex='^[a-zA-Z0-9]*$',
                    message='El nombre de usuario solo puede contener letras y números',
                    code='invalid_username'
                )
            ]
        }
    
class RegisterAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

class GuestLoginForm(AuthenticationForm):
    accept_privacy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

class RegisterAccommodation(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'capacity', 'price', 'category', 'service']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

        help_texts = {
            'name': None,
            'description': None,
            'capacity': None,
            'price': True,
            'category': None,
        }

        validators={
            'price': [
                RegexValidator(
                    regex='^[1-9]\d*(\.\d{1,2})?$',
                    message='El precio debe ser un número decimal estrictamente positivo',
                    code='invalid_price'
                )
            ]
        },

        

        


