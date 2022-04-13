from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from configuracion.models import *


DEFAULT_ID = 1







class Permisos(models.Model):

    id = models.IntegerField(primary_key=True)
    usuario = models.OneToOneField(User, default=1)

    pacientes = models.BooleanField(default=True)
    administrador = models.BooleanField(default=True)

    territorios = models.BooleanField(default=True)
    entidades = models.BooleanField(default=True)
    personas  = models.BooleanField(default=True)
    salud = models.BooleanField(default=True)

    gestion_entidad = models.BooleanField(default=True)
    medicamento = models.BooleanField(default=True)

    reporte_general = models.BooleanField(default=True)
    reporte_balance = models.BooleanField(default=True)


class Usuarios_datos(models.Model):

    id = models.IntegerField(primary_key=True)
    usuario = models.ForeignKey(User, default=1)

    empresa = models.ForeignKey(Empresas, default=1)
    dependencias = models.ForeignKey(Dependencias, default=1)
    cedula = models.CharField(max_length=45, null=True)
    fecha_nacimiento = models.DateField(null=True)
    ubicacion = models.CharField(max_length=45, null=True)
    piso = models.IntegerField(default=1)
    extension = models.IntegerField(default=1)
    estado = models.CharField(max_length=45, null=True)
    publico = models.BooleanField(default=True)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)


class HistoriaUsuario(models.Model):
    usuario=models.ForeignKey(Usuarios_datos, default=1)
    empresa=models.ForeignKey(Empresas, default=1)
    accion=models.CharField(max_length=100, null=True)
    fecha=models.DateField(null=True)