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
    telefono = models.CharField(max_length=45, null=True)
    cargo = models.CharField(max_length=45, null=True)
    admin = models.BooleanField(default=True)
    atencion = models.IntegerField(default=1)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)


class HistoriaUsuario(models.Model):
    usuario=models.ForeignKey(Usuarios_datos, default=1)
    empresa=models.ForeignKey(Empresas, default=1)
    accion=models.CharField(max_length=100, null=True)
    fecha=models.DateTimeField(null=True)


class HistorialErrorTarea(models.Model):
    accion=models.CharField(max_length=100, null=True)
    pedido=models.CharField(max_length=100, null=True)
    empresa=models.CharField(max_length=100, null=True)
    fecha=models.DateField(null=True)
    hora=models.TimeField(null=True)


class HistorialErrorApi(models.Model):
    accion=models.CharField(max_length=100, null=True)
    pedido=models.CharField(max_length=100, null=True)
    empresa=models.CharField(max_length=100, null=True)
    fecha=models.DateField(null=True)
    hora=models.TimeField(null=True)

class ClientesApi(models.Model):
    NombreEmpresa = models.CharField(max_length=100, null=True)
    Identificacion = models.CharField(max_length=100, null=True)
    TipoIdentificacion = models.CharField(max_length=100, null=True)
    Correo = models.CharField(max_length=100, null=True)
    ValorOrden = models.CharField(max_length=100, null=True)
    FechaEntrega = models.DateField( null=True)
    FechaPago = models.DateField(null=True)
    FechaHoy = models.DateField(null=True)
    NumeroPedido = models.CharField(max_length=100, null=True)

class FacturasApi(models.Model):
    NombreEmpresa = models.CharField(max_length=100, null=True)
    Identificacion = models.CharField(max_length=100, null=True)
    TipoIdentificacion = models.CharField(max_length=100, null=True)
    Correo = models.CharField(max_length=100, null=True)
    ValorOrden = models.CharField(max_length=100, null=True)
    FechaPago = models.DateField(null=True)
    FechaHoy = models.DateField(null=True)
    NumeroPedido = models.CharField(max_length=100, null=True)