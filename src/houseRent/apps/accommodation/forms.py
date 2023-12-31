from django import forms
from apps.core.models import Accommodation, Image, Claim
from django.core.validators import RegexValidator

class RegisterAccommodation(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'capacity', 'price', 'category', 'service','is_active']

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

class RegisterImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'alt']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'alt': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model= Claim
        fields=['response']

        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control'})
        }

        labels = {
            'response': 'Respuesta ante la reclamación'
        }