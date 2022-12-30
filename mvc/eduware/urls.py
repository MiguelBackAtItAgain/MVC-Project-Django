from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('student/home', views.studentLogin, name='Student home page'),
    path('teacher/home', views.teacherLogin, name='Teacher home page'),
    path('error', views.error, name="Error"),
    path('teacher/challenges', views.getChallenges, name='getChallengesTeachers'),
    path('student/challenges', views.getChallenges, name='getChallengesStudents'),
    path('teacher/challenges/create_challenge', views.createChallenge, name='createChallenge'),
    path('student/challenge/add_solution', views.addSolution, name='addSolution'),
    path('student/challenge/view_solutions', views.getSolutions, name='getSolutionsStudent'),
    path('teacher/challenge/view_solutions', views.getSolutions, name='getSolutionsTeacher'),
    path('teacher/challenge/grade_challenge', views.gradeChallenge, name='gradeChallenge'),
    path('teacher/challenges/get_grades', views.getGrades, name='getGradesTeachers'),
    path('student/challenges/get_grades', views.getGrades, name='getGradesStudents'),
    path('teacher/decils', views.calculateDecils, name='calculateDecils')
]
