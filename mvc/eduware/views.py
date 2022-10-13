from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from .models import Teacher as t, Student as s
from .forms import StudentUploadForm, StudentLoginForm
""""We import the UserCreationForm in order for it to be used in the Register method"""

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
            return render(request, "eduware/student_list.html")
    form = StudentUploadForm(request.POST)
    return render(request, "eduware/register.html", {'form' : StudentUploadForm})

def login(request):
    if request.POST:
        form = StudentLoginForm(request.POST)
        if form.is_valid:
            return render(request, "eduware/welcome.html")
    return render(request, "eduware/login.html",{'form' : StudentLoginForm } )
