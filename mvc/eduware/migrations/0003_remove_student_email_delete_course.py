# Generated by Django 4.1.1 on 2022-10-04 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eduware', '0002_student_subject_alter_teacher_options_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
