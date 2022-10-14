from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name="student_login"),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name="welcome"),
    path('students/', views.students_list, name='student_list'),
    path('teachers/', views.teachers_list, name='teacher_list')
]
