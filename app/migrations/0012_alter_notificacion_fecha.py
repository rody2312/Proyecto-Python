# Generated by Django 4.0.3 on 2022-08-25 19:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_notificacion_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='fecha',
            field=models.DateField(blank=True, default=django.utils.timezone.now, editable=False),
        ),
    ]
