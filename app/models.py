# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator



# Clase para definir funciones de crear usuarios en el sistema por comando
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        #if not full_name:
        #    raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        #user.full_name = full_name
        user.set_password(password)  # change password to hash
        #user.profile_picture = profile_picture
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        #if not full_name:
        #    raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.nombre = "Cecilia"
        user.apellido_paterno = "Vergara"
        user.apellido_materno = "Cortes"
        user.fono = "999999999"
        user.id_tipo_usuario = TipoUsuario.objects.get(pk=1)
        user.set_password(password)
        #user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


# Aca se definen los modelos

class TipoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_usuario'

    def __str__(self):
        return self.tipo
    



class Usuario(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    id_tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='id_tipo_usuario')
    nombre = models.CharField(max_length=20, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=30, blank=True, null=True)
    apellido_materno = models.CharField(max_length=30, blank=True, null=True)
    fono = models.IntegerField(blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50,unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        managed = True
        db_table = 'usuarios'
    
    def __str__(self):
        return self.nombre + " " + self.apellido_paterno + " " + self.apellido_materno


#### Tablas de Notificaciones #####
class Notificacion(models.Model):
    enviado_por = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='enviado_por', default=1)
    asunto = models.CharField(max_length=40, default='asunto')
    texto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now, editable=False, blank=True)

    class Meta():
        managed = True
        db_table = 'notificacion'


class EstadoNotificacion(models.Model):
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta():
        managed = True
        db_table = 'estado_notificacion'


class NotificacionEnviada(models.Model):
    notificacion = models.ForeignKey(Notificacion, models.SET_NULL, null=True, db_column='notificacion')
    enviado_a = models.ForeignKey(Usuario, models.SET_NULL, null=True, db_column='enviado_a')
    estado = models.ForeignKey(EstadoNotificacion, models.SET_NULL, null=True, db_column='estado', default=1)

    class Meta():
        managed = True
        db_table = 'notificacion_enviada'









