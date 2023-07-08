from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    )

    PRIORIDAD_CHOICES = (
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    )

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    asignado_a = models.ForeignKey(User, related_name='tareas_asignadas', on_delete=models.CASCADE, default=1)
    prioridad = models.CharField(max_length=12, choices=PRIORIDAD_CHOICES)

    def __str__(self):
        return self.titulo
    
from django.db import models

class Prioridad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
