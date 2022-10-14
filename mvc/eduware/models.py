from tkinter import CASCADE
from django.db import models
from datetime import date

# Create your models here.

class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=5)
    personalid = models.CharField(max_length=10)
    email = models.EmailField(default='error@notcorrectlygenerated.com')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"id: {self.id}, {self.name}, school id: {self.schoolid}"

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    parentphonenum = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    password = models.CharField(max_length=20)
    birthdate = models.DateField()
    email = models.EmailField(default='error@notcorrectlygenerated.com')

    class Meta:
        ordering = ['name']

    def __int__(self):
        return self.pk

class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    nrc = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, nrc: {self.nrc}"

class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    coursenumber = models.IntegerField()
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)

    class Meta:
        ordering = ['coursenumber']
    
    def get_all_courses(self):
        return Course.objects.select_related('Student', 'Subject', 'Teacher')

class StudentSession(models.Model):
    id = models.IntegerField(primary_key=True)
    session_state = models.CharField(max_length=1)
    alternate_id = models.IntegerField()
    date = models.DateField()
    student = models.ForeignKey("Student", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
    
    def get_session(self):
        return StudentSession.objects.select_related('Student', 'State', 'Date')


