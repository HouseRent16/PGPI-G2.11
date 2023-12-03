from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import CustomUser, Address
from django_countries.fields import CountryField

class AdminPasswordChangeForm(SetPasswordForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
class CustomUserForm(forms.ModelForm):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'input'}, initial='ES'))
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
        

    # def save(self, commit=True):
    #     user = super(CustomUserForm, self).save(commit=False)

    #     #Habría que comprobar que la contraseña sea la misma
    #     if self.cleaned_data['password']:
    #         user.set_password(self.cleaned_data.get['password'])
        
    #     user.phone = self.cleaned_data['phone']

    #     if commit:
    #         user.save()
    #     return user

class AddressForm(forms.ModelForm):
    country = CountryField().formfield(widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = Address
        fields = ['street_number', 'address_line', 'country', 'region', 'city', 'postal_code']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})