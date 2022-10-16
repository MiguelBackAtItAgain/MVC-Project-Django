from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Teacher as t, Student as s, StudentSession as ss
from .forms import StudentUploadForm, StudentLoginForm
import random
from datetime import date

""""We import the UserCreationForm in order for it to be used in the Register method"""

# Create your views here.
def teachers_list(request):
    list = t.objects.order_by('name')
    return render(request, 'eduware/teacher_list.html', {'teachers' : list})

def students_list(request):
    list = s.objects.order_by('name')
    return render(request, 'eduware/student_list.html', {'students' : list})

def welcome(request):
    if request.session.has_key('session_id'):
        alt_id = request.session['session_id']
        student_session = ss.objects.filter(alternate_id=alt_id).first()
        student = student_session.student
        return render(request, "eduware/welcome.html", {'student' : student})
    else:
        return render(request, "eduware/error_view.html")

def register(request):
    if request.POST:
        form = StudentUploadForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('student_login')
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
                student_session = ss(session_state='A', alternate_id=alt_id, date=date.today(), student=user)
                student_session.save()
                request.session['session_id'] = student_session.alternate_id
                return redirect('welcome')
            else:
                print("Incorrect data, try again!")
    return render(request, "eduware/student_login.html",{'form' : StudentLoginForm } )

def error(request):
    return render(request, "eduware/error")

