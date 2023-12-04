from django import forms
from django.contrib.auth.forms import SetPasswordForm
from apps.core.models import Comment, Claim


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
