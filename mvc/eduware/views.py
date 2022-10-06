from django.shortcuts import render
from .models import Teacher as t, Student as s
from django.shortcuts import redirect

# Create your views here.
def teachers_list(request):
    list = t.objects.order_by('name')
    return render(request, 'eduware/teacher_list.html', {'teachers' : list})

def students_list(request):
    list = s.objects.order_by('name')
    return render(request, 'eduware/student_list.html', {'students' : list})

def welcome(request):
    return render(request, "eduware/welcome.html")

