# Generated by Django 4.1.1 on 2022-12-16 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import eduware.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('idnumber', models.CharField(max_length=10, unique=True, validators=[eduware.models.only_int], verbose_name='ID number')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('phonenum', models.CharField(max_length=10, unique=True, validators=[eduware.models.only_int], verbose_name='Phone number')),
                ('gender', models.CharField(max_length=1, verbose_name='Gender')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=1000)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coursenumber', models.IntegerField()),
                ('parallel', models.CharField(max_length=1)),
                ('max_students', models.IntegerField()),
            ],
            options={
                'ordering': ['coursenumber'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.FloatField()),
                ('points', models.IntegerField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.challenge')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=1000)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.grade')),
                ('student_in_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.studentcourse')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='challenge',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduware.course'),
        ),
    ]
