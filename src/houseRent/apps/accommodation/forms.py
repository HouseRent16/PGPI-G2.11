from django import forms
from apps.core.models import Accommodation
from django.core.validators import RegexValidator

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
        }