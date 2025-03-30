# Generated by Django 5.1.7 on 2025-03-27 23:22

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id_contrato', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('terminos', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id_proyecto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id_tarea', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en progreso', 'En Progreso'), ('completada', 'Completada')], default='pendiente', max_length=15)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='gestion.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='SeguimientoTiempo',
            fields=[
                ('id_tiempo', models.AutoField(primary_key=True, serialize=False)),
                ('inicio', models.DateTimeField()),
                ('fin', models.DateTimeField(blank=True, null=True)),
                ('duracion', models.IntegerField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to='gestion.tarea')),
            ],
        ),
    ]
