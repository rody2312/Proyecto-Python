# Generated by Django 4.0.3 on 2022-06-12 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'actividad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tipo_actividad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoForo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tipo_foro',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('id_actividad', models.ForeignKey(db_column='id_actividad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tareas.actividad')),
                ('id_tipo_foro', models.ForeignKey(db_column='id_tipo_foro', on_delete=django.db.models.deletion.PROTECT, to='tareas.tipoforo')),
            ],
            options={
                'db_table': 'foro',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('directorio', models.CharField(max_length=200)),
                ('id_usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'archivo',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='actividad',
            name='id_tipo_actividad',
            field=models.ForeignKey(db_column='id_tipo_actividad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tareas.tipoactividad'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='id_usuario',
            field=models.ForeignKey(db_column='id_usuario', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
