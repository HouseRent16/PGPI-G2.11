from django import forms
from apps.core.models import Comment, Claim

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write comment"}))

    class Meta:
        model = Comment
        fields = ['comment', 'rating']
