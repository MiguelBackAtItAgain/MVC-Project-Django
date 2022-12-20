from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('student/home', views.studentLogin, name='Student home page'),
    path('teacher/home', views.teacherLogin, name='Teacher home page')
]
