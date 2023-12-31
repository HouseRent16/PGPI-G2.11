from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import CustomUser, Address,Comment, Claim
from django_countries.fields import CountryField

class AdminPasswordChangeForm(SetPasswordForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Comment
        fields = ['title', 'description', 'rating']

        widgets={
        'title': forms.Textarea(attrs={'class': 'form-control custom-title-input', 'required': True}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
        'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

        labels={
            'title': 'Título',
            'description': "Descripción",
            'rating': "Valoración (1-5)"


        }


class ClaimForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Claim
        fields = ['title', 'description']

        widgets={
        'title': forms.Textarea(attrs={'class': 'form-control custom-title-input', 'required': True}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
        }

        labels={
            'title': 'Título',
            'description': "Reclamación",
        }

class CustomUserForm(forms.ModelForm):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'input'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        required=True, 
        label='Password'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'phone', 'dni', 'gender']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        

class AddressForm(forms.ModelForm):
    country = CountryField().formfield(widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = Address
        fields = ['street_number', 'address_line', 'country', 'region', 'city', 'postal_code']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
