from django.forms import ModelForm
from django import forms
from .models import Student as s

class StudentUploadForm(ModelForm):
    name = forms.TextInput()
    parentphonenum = forms.TextInput(attrs={'type':'number'})
    gender = forms.TextInput()
    password = forms.TextInput()
    birthdate = forms.DateField()
    email = forms.EmailField()
    class Meta:
        model = s
        fields = ['name', 'parentphonenum', 'gender', 'birthdate', 'email', 'password']