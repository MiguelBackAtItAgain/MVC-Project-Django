from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Teacher as t, Student as s, StudentSession as ss
from .forms import StudentUploadForm, StudentLoginForm
import random
from datetime import date

""""We import the UserCreationForm and User model in order for them to be used in the Register method"""

# Create your views here.
def teachers_list(request):
    list = t.objects.order_by('name')
    return render(request, 'eduware/teacher_list.html', {'teachers' : list})

def students_list(request):
    list = s.objects.order_by('name')
    return render(request, 'eduware/student_list.html', {'students' : list})

def welcome(request):
    if request.user.is_authenticated:
        user = request.user
        student = s.objects.filter(email=user.email).first()
        return render(request, "eduware/welcome.html", {'student' : student})
    else:
        return render(request, "eduware/error_view.html")

def register(request):
    if request.POST:
        studentform = StudentUploadForm(request.POST)
        print(request.POST)
        if studentform.is_valid():
            studentform.save()
            userform = User.objects.create_user(username=request.POST['name'], email=request.POST['email'],
                                                password=request.POST['password'], date_joined= date.today())
            userform.save()
            return redirect('student_login')
    form = StudentUploadForm(request.POST)
    return render(request, "eduware/register.html", {'form' : StudentUploadForm})

def student_login(request):
    if request.POST:
        form = StudentLoginForm(request.POST)
        if form.is_valid:
            student_email = request.POST['email']
            student_password = request.POST['password']
            student = s.objects.filter(email=student_email).first()
            if student is not None:
                user = authenticate(username=student.name, password=student_password)
                if user is not None:
                    login(request, user)
                    return redirect('welcome')
                else:
                    print("You used to be a student but now there is no associated account to you.")
            else:
                print("Incorrect data, try again!")
    if request.user.is_authenticated:
        return redirect('welcome')
    return render(request, "eduware/student_login.html",{'form' : StudentLoginForm } )

def student_logout(request):
    logout(request)
    return redirect('student_login')

def error(request):
    return render(request, "eduware/error")

