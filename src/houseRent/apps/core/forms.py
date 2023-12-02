from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import CustomUser

class AdminPasswordChangeForm(SetPasswordForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
class UserForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'input'}, initial='ES')
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'phone', 'password', 'dni', 'gender']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'birth_date': forms.DateInput(attrs={'class': 'input'}),
            'dni': forms.TextInput(attrs={'class': 'input'}),
            'gender': forms.Select(attrs={'class': 'input'}),
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
