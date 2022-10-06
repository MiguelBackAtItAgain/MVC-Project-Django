from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teachers_list, name='teacher_list'),
    path('students/', views.students_list, name='student_list'),
    path('', views.welcome)
]
