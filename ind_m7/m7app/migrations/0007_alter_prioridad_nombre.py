# Generated by Django 4.2.3 on 2023-07-08 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m7app', '0006_tarea_prioridad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prioridad',
            name='nombre',
            field=models.CharField(choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')], max_length=100),
        ),
    ]
