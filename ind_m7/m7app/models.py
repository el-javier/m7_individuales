from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Definiendo la clase para las tablas de usuario , recogeran datos de nombre, email, edad y fecha de creacion.

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

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

