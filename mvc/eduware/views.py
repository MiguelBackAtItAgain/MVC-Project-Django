from django.shortcuts import render
from django.shortcuts import redirect
from .models import Teacher as t

# Create your views here.
def teachers_list(request):
    list = t.objects.order_by('name')
    return render(request, 'eduware/teacher_list.html', {'teachers' : list})