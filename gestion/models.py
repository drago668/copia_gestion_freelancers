from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, max_length=100)
    #contrasena = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith('pbkdf2_'):  # Si es nuevo o no está encriptada
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contratos')
    nombre_cliente = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    terminos = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.nombre_cliente}"

class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proyectos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en progreso', 'En Progreso'),
        ('completada', 'Completada')
    ]

    id_tarea = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class SeguimientoTiempo(models.Model):
    id_tiempo = models.AutoField(primary_key=True)
    id_tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='seguimientos')
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)  # En minutos
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seguimiento {self.id_tiempo} - Tarea {self.id_tarea}"
# Create your models here.
