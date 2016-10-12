__author__ = 'wanyama'
from django import forms
from core.models import BusinessPhoto

class BusinessPhotoForm(forms.ModelForm):
    photo = forms.ImageField()
    class Meta:
        model=BusinessPhoto
        fields = ('photo')

