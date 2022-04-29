# Generated by Django 4.0.3 on 2022-04-28 04:26

from django.db import migrations


class Migration(migrations.Migration):

    def insert_default_data(apps, schema_editor):
        # We can't import the Person model directly as it may be a newer
        # version than this migration expects. We use the historical version.
        TipoArchivo = apps.get_model("tareas", "TipoArchivo")
        tipoArchivo=TipoArchivo(tipo="Tarea")
        tipoArchivo.save()
        tipoArchivo=TipoArchivo(tipo="Material de estudio")
        tipoArchivo.save()

        PuntajeArchivo = apps.get_model("tareas", "PuntajeArchivo")
        puntajeArchivo=PuntajeArchivo(puntaje="30")
        puntajeArchivo.save()
        puntajeArchivo=PuntajeArchivo(puntaje="50")
        puntajeArchivo.save()
        puntajeArchivo=PuntajeArchivo(puntaje="100")
        puntajeArchivo.save()



    dependencies = [
        ('tareas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_default_data),
    ]