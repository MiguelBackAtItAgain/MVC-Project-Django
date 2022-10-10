from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=5)
    personalid = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, school id: {self.schoolid}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    parentphonenum = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    password = models.CharField(max_length=20)
    birthdate = models.DateField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, gender: {self.gender}, birthdate: {self.birthdate}, representative number: {self.parentphonenum}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    nrc = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, nrc: {self.nrc}"

class Course(models.Model):
    coursenumber = models.IntegerField()
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)

    class Meta:
        ordering = ['coursenumber']
    
    def get_all_courses(self):
        return Course.objects.select_related('Student', 'Subject', 'Teacher')
