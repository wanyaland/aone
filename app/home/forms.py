from django import forms
from .models import ContactUsRequest


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsRequest
        fields = ['name', 'email', 'subject', 'message']