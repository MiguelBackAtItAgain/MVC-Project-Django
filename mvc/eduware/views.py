from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Teacher as t, Student as s, StudentSession as ss
from .forms import StudentSessionForm, StudentUploadForm, StudentLoginForm
import random
from datetime import date

""""We import the UserCreationForm and StudentLoginForm in order for it to be used in the Register method"""

# Create your views here.
def teachers_list(request):
    list = t.objects.order_by('name')
    return render(request, 'eduware/teacher_list.html', {'teachers' : list})

def students_list(request):
    list = s.objects.order_by('name')
    return render(request, 'eduware/student_list.html', {'students' : list})

def welcome(request):
        return render(request, "eduware/welcome.html")

def register(request):
    if request.POST:
        form = StudentUploadForm(request.POST)
        if form.is_valid():
            print(request.POST)   
            form.save()
            return render(request, "eduware/student_login.html")
    form = StudentUploadForm(request.POST)
    return render(request, "eduware/register.html", {'form' : StudentUploadForm})

def student_login(request):
    if request.POST:
        form = StudentLoginForm(request.POST)
        if form.is_valid:
            user_email = request.POST['email']
            user_password = request.POST['password']
            user = s.objects.filter(email = user_email, password=user_password).first()
            if user is not None:
                alt_id = random.randint(50000, 1000000)
                student_session = StudentSessionForm('A', alt_id, date.today(), user.id)
                student_session.save()
            else:
                print("Incorrect data, try again!")
    return render(request, "eduware/student_login.html",{'form' : StudentLoginForm } )
