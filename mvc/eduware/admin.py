from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ua
from django import forms
from .models import Subject as sb, Course as c, SchoolClass as sc, StudentList as sl, User as s
# Register your models here.

@admin.register(sb)
class SubjectAdmin(admin.ModelAdmin):
    """Subject admin"""
    list_display = ('id', 'name')

@admin.register(c)
class CourseAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "%s" % (obj.name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            return self.CustomModelChoiceField(queryset=s.objects)
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    """Course admin"""
    list_display = ('coursenumber', 'parallel', 'teacher', 'subject')

@admin.register(sc)
class ClassAdmin(admin.ModelAdmin):
    
    """Class admin"""
    list_display = ('id', 'max_students')

@admin.register(sl)
class StudentListAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "%s" % (obj.name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            return self.CustomModelChoiceField(queryset=s.objects)
        return super(StudentListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    """Student in class admin"""
    list_display = ('id', 'student', 'schoolclass')

################################################################################

class UserAdmin(admin.ModelAdmin):


    fieldsets = (
        (None, {
            'fields': ('username', 'name','idnumber', 'address', 'email', 'phonenum', 'gender', 'birthdate', 'password')
        }),
        ('Permissions', {
            'classes': ['wide'],
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups')
        }),
    )

    list_display = ('name', 'email', 'gender', 'birthdate')

    filter_horizontal = ('groups', 'user_permissions',)




admin.site.register(s, UserAdmin)

