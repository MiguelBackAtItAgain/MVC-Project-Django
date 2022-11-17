from tkinter import CASCADE
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.

def only_int(value):
        if value.isdigit()== False:
            raise ValidationError('ID contains characters.')

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    idnumber = models.CharField(max_length=10, validators=[only_int])
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenum = models.CharField(max_length=10, validators=[only_int])
    gender = models.CharField(max_length=1)
    birthdate = models.DateField()

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, nrc: {self.nrc}"


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    coursenumber = models.IntegerField()
    parallel = models.CharField(max_length=1)
    teacher = models.ForeignKey("User", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)

    class Meta:
        ordering = ['coursenumber']


class SchoolClass(models.Model):
    id = models.AutoField(primary_key=True)
    max_students = models.IntegerField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)



class StudentList(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey("User", on_delete=models.CASCADE)
    schoolclass = models.ForeignKey("SchoolClass", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
