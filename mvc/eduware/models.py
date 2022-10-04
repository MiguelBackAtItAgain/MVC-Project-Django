from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=5)
    personalid = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, school id: {self.schoolid} | e-mail: {self.email}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=40)
    parentphonenum = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
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
    gradenumber = models.IntegerField()
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)
    subject = models.ManyToManyField(Subject)

    class Meta:
        ordering = ['gradenumber']
    
    def get_all_courses(self):
        return Course.objects.select_related('Student', 'Subject', 'Teacher')



    




