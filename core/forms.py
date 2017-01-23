__author__ = 'wanyama'

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput,EmailInput
from models import Customer,Business,Review,BusinessPhoto
from django.forms.widgets import RadioFieldRenderer
from django.core.exceptions import *

class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]

class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size' : u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return
        elif self.max_num and  num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
        for uploaded_file in data:
            if uploaded_file.size > self.maximum_file_size:
                raise ValidationError(self.error_messages['file_size'] % { 'uploaded_file_name': uploaded_file.name})

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1':TextInput(attrs={'class':'form-control','placeholder': 'Password'}),
            'password2':TextInput(attrs={'class': 'form-control','placeholder': 'Repeat Password'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['photo']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields =('name','address','email','web_address','phone_number','city','categories','photo')
        widgets = {
            'name':TextInput(attrs={'class':'form-control','placeholder':'Business Name'}),
            'address':TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'email':EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'city':TextInput(attrs={'class':'form-control','placeholder':'City'}),
            'phone_number':TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'web_address':TextInput(attrs={'class':'form-control','placeholder':'Web Address'}),
            'categories':forms.CheckboxSelectMultiple(),
        }

class ReviewForm(forms.ModelForm):
    rating = forms.CharField(widget=forms.NumberInput(attrs={'class':'rating','data-min':'1','data-max':'5','step':'0.5','type':'number','id':'input-id','data-size':'xs',}))
    files = MultiFileField(max_num=5,min_num=1,maximum_file_size=1024*1024*5)
    class Meta:
        model = Review
        fields = ('rating','review',)

class BusinessSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Near:'}))

class PhotoForm(forms.ModelForm):
    class Meta:
        model=BusinessPhoto
        fields=('photo',)

class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change their password without entering the old password
    """
    error_messsages = {
            'password_mismatch': ("The two password fields do not match"),
            }
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1!=password2:
                raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code = 'password_mismatch',
                        )
            return password2

