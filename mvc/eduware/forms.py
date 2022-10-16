from django.forms import ModelForm
from django import forms
from .models import Student as s, StudentSession as ss


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

class StudentLoginForm(ModelForm):
    email = forms.EmailField()
    password = forms.TextInput()
    class Meta:
        model = s
        fields = ['email', 'password']

class StudentSessionForm(ModelForm):
    session_state = forms.TextInput()
    alternate_id = forms.IntegerField()
    date = forms.DateField()
    student = forms.IntegerField()

    def __init__(self, state, alt_id, date, student):
        self.session_state = state
        self.alternate_id = alt_id
        self.date = date,
        self.student = student
        super().__init__()
    class Meta:
        model = ss
        fields = ['session_state', 'alternate_id', 'date', 'student']


        
        

