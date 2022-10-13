from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name="welcome"),
    path('students/', views.students_list, name='student_list'),
    path('teachers/', views.teachers_list, name='teacher_list')
]
