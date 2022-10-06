from django.contrib import admin
from .models import Teacher as t, Student as s

# Register your models here.

@admin.register(t)
class TeacherAdmin(admin.ModelAdmin):
    """Teacher admin"""
    list_display = ('id', 'name', 'schoolid', 'personalid')

@admin.register(s)
class StudentAdmin(admin.ModelAdmin):
    """Teacher admin"""
    list_display = ('id', 'name', 'parentphonenum', 'gender', 'birthdate')
