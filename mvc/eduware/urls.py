from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('register/', views.register, name='register'),
    path('login/', views.login),
    path('students/', views.students_list, name='student_list'),
    path('teachers/', views.teachers_list, name='teacher_list'),
]
