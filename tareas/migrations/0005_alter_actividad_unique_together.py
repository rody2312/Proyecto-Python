# Generated by Django 4.0.3 on 2022-06-20 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0004_alter_usuarioactividad_puntaje'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='actividad',
            unique_together={('fecha', 'id_tipo_actividad')},
        ),
    ]
