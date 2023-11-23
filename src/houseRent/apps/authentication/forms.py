from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from apps.core.models import CustomUser, Address
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterUser(forms.ModelForm):
    class Meta:
        model = CustomUser

        exclude = ['request','is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 'is_active', 'address']
        fields = "__all__"

        birthDate = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
        phone = forms.CharField(max_length=9, required=False)
        address = forms.ModelChoiceField(queryset=Address.objects.all(), required=False)
        dni = forms.CharField(max_length=9, validators=[RegexValidator(
            regex='^\d{8}[a-zA-Z]$', message='Introduzca un DNI válido', code='invalid_chart_field')])
        gender = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
        isOwner = forms.BooleanField(required=False)

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        # Puedes realizar validaciones adicionales para el DNI si es necesario
        return dni
    
class RegisterAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

class GuestLoginForm(AuthenticationForm):
    accept_privacy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


