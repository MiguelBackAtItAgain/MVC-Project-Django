from django.shortcuts import render
from .models import Teacher as t
from django.contrib.auth.forms import UserCreationForm 
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
    """"A default form is used through the exporting of this view."""
    form = UserCreationForm()
    """"It is later passed as a value for a dictionary (whose name is "context") in order for it to be used in the views."""
    context = {'form':form}
    """"Finally, the context in question is passed as the third parameter."""
    return render(request, "eduware/register.html", context)

def login(request):
    return render(request, "eduware/login.html")
