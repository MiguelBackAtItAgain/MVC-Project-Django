from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as ua
from django import forms

from .models import Subject as sb, Course as c,  StudentCourse as sc, User as s
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.

User = get_user_model()

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
class StudentCourseAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "%s" % (obj.name)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            return self.CustomModelChoiceField(queryset=s.objects)
        return super(StudentCourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    """Student in class admin"""
    list_display = ('id', 'student')
    

################################################################################

class UserAdmin(ua):
    
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email']
    list_filter = ['admin']

    fieldsets = (
        ('Student info', {'fields': ('email', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('name', 'idnumber', 'address', 'email', 'phonenum', 'gender', 'birthdate', 'password', 'password_2')
        }),
        ('Permissions', {'fields': ('admin', 'groups',)}),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)