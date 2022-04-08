# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TipoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_usuario'
    


class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='id_tipo_usuario')
    nombre = models.CharField(max_length=20, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=30, blank=True, null=True)
    apellido_materno = models.CharField(max_length=30, blank=True, null=True)
    fono = models.IntegerField(blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    clave = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
