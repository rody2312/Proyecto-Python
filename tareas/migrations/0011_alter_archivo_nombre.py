# Generated by Django 4.0.3 on 2022-08-25 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0010_alter_archivo_fecha_delete_foro_delete_tipoforo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
