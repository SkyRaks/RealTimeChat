from django.forms import ModelForm
from django import forms
from .models import Profile

class ProflileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = ['image', 'displayname', 'info']
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(),
            'displayname': forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'info': forms.TextInput(attrs={'rows': 3, 'placeholder': 'Add info'})
        }
