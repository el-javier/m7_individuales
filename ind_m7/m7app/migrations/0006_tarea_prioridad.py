# Generated by Django 4.2.3 on 2023-07-08 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('m7app', '0005_prioridad'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='prioridad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='m7app.prioridad'),
        ),
    ]
