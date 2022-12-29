from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import *

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):

    '''Used to create a new user from the admin pannel. It includes all fields together with password validation.'''

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label = "Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']
    
    def clean(self):
        '''Used to verify whether both passwords match.'''
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords don't match")
        return cleaned_data
    
    def save(self, commit=True):
        '''Used to save the provided password in hashed format.'''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    '''Form used to update users. It includes all the fields on the user and replaces the
    password field with the admin password's display field'''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']
    
    def clean_password(self):
        '''Regardless of what the user provides, it returns the initial value. This is done here as
        the field in question doesn't have access to the initial value.'''
        return self.initial['password']

class ChallengeCreationForm(forms.ModelForm):
    title = forms.TextInput()
    description = forms.TextInput()
    answer = forms.TextInput()
    begin_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        course_id = None
        if 'course_id' in kwargs:
            course_id = kwargs.pop('course_id')
        super(ChallengeCreationForm, self).__init__(*args, **kwargs)
        if course_id:
            self.fields['course'].initial = course_id

    class Meta:
        model = Challenge
        fields = ['title', 'description', 'answer', 'begin_date', 'end_date', 'course']

class AddSolutionForm(forms.ModelForm):
    answer = forms.TextInput()
    student_in_course = forms.ModelChoiceField(queryset=StudentCourse.objects.all(), widget=forms.HiddenInput())
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        student_in_course_id = None
        challenge_id = None
        if 'student_in_course_id' in kwargs and 'challenge_id' in kwargs: 
            student_in_course_id = kwargs.pop('student_in_course_id')
            challenge_id = kwargs.pop('challenge_id')
        super(AddSolutionForm, self).__init__(*args, **kwargs)
        if student_in_course_id and challenge_id:
            self.fields['student_in_course'].initial = student_in_course_id
            self.fields['challenge'].initial = challenge_id
    
    class Meta:
        model = Solution
        fields = ['answer', 'student_in_course', 'challenge']
    
class gradeSolutionForm(forms.ModelForm):
    grade = forms.FloatField(validators=[MaxValueValidator(100.0), MinValueValidator(10.0)])
    points = forms.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], widget=forms.HiddenInput())
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.all(), widget=forms.HiddenInput())
    solution =forms.ModelChoiceField(queryset=Solution.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        challenge_id = None
        solution_id = None
        if 'challenge_id' in kwargs and 'solution_id' in kwargs:
            challenge_id = kwargs.pop('challenge_id')
            solution_id = kwargs.pop('solution_id')
        super(gradeSolutionForm, self).__init__(*args, **kwargs)
        if challenge_id  and solution_id:
            self.fields['challenge'].initial = challenge_id
            self.fields['solution'].initial = solution_id

    class Meta:
        model = Grade
        fields = ['grade', 'points', 'challenge', 'solution']