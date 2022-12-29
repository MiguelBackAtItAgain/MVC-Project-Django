from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.


def only_int(value):
        if value.isdigit()== False:
            raise ValidationError('ID contains characters.')


class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):   
        
        if not email:
            raise ValueError('The given email must be set')
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )

        if not password:
            raise ValueError("Users must have a password.")
         
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('admin', True)
        return self.create_user(email, password, **extra_fields)
    
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Name", max_length=100)
    idnumber = models.CharField(verbose_name="ID number", max_length=10, unique=True, validators=[only_int])
    address = models.CharField(verbose_name="Address", max_length=100)
    email = models.EmailField(verbose_name="E-mail", unique=True)
    phonenum = models.CharField(verbose_name="Phone number", max_length=10, validators=[only_int], unique=True)
    gender = models.CharField(verbose_name="Gender", max_length=1)
    birthdate = models.DateField(verbose_name="Birthdate")
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    objects = UserManager()

    class Meta:
        ordering = ['id']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'idnumber', 'address', 'phonenum', 'gender', 'birthdate']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    coursenumber = models.IntegerField()
    parallel = models.CharField(max_length=1)
    teacher = models.ForeignKey("User", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    max_students = models.IntegerField()

    class Meta:
        ordering = ['coursenumber']

    def __str__(self):
        return f"{self.subject.name  + ' | ' + str(self.coursenumber) + ' ' + self.parallel + ' | ' + self.teacher.name}"


class StudentCourse(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey("User",  on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    def __unicode__(self):
        return u'%s %s' 

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.student.name, self.course.coursenumber}"

class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    begin_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.title, self.description, str(self.begin_date), str(self.end_date)}"

class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=1000)
    student_in_course = models.ForeignKey("StudentCourse", on_delete=models.CASCADE)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.student_in_course.student.name, self.challenge.title, self.answer}"

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.FloatField()
    points = models.IntegerField()
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)
    solution = models.ForeignKey("Solution", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


