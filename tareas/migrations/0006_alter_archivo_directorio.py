# Generated by Django 4.0.3 on 2022-06-23 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0005_alter_actividad_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='directorio',
            field=models.FileField(max_length=200, upload_to=''),
        ),
    ]
