# Generated by Django 4.0.3 on 2022-06-22 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0005_alter_actividad_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='id_tipo_actividad',
            field=models.ForeignKey(db_column='id_tipo_actividad', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='actividades_tipos', to='tareas.tipoactividad'),
        ),
    ]
