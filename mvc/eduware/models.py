from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=5)
    personalid = models.CharField(max_length=10)