from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add Message...', 'max_length': '300', 'autofocus': True}),
        }
