# Generated by Django 4.0.3 on 2022-04-26 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_notificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
    ]