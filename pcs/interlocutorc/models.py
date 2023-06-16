from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

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


class Perfiles_PCS(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    codigo_conecta = models.CharField(max_length=100, null=True)
    comercial_direccion = models.BooleanField(default=True)
    exportaciones_direccion = models.BooleanField(default=True)
    desarrollo_empresarial_direccion = models.BooleanField(default=True)
    administrativo_financiero_direccion = models.BooleanField(default=True)
    mercadeo_innovacion_direccion = models.BooleanField(default=True)
    operaciones_logistica_direccion = models.BooleanField(default=True)
    comercial_coordinacion_1= models.BooleanField(default=True)
    comercial_coordinacion_2 = models.BooleanField(default=True)
    exportaciones_Coordinacion_1 = models.BooleanField(default=True)
    desarrollo_empresarial_coordinacion_1 = models.BooleanField(default=True)
    desarrollo_empresarial_coordinacion_2 = models.BooleanField(default=True)
    administrativo_financiero_coordinacion_1 = models.BooleanField(default=True)
    administrativo_financiero_coordinacion_2 = models.BooleanField(default=True)
    administrativo_financiero_coordinacion_3 = models.BooleanField(default=True)
    mercadeo_innovacion_coordinacion_1 = models.BooleanField(default=True)
    mercadeo_innovacion_coordinacion_2 = models.BooleanField(default=True)
    operaciones_logistica_coordinacion_1 = models.BooleanField(default=True)
    operaciones_logistica_coordinacion_2 = models.BooleanField(default=True)
    comercial_analista_senior_1 = models.BooleanField(default=True)
    comercial_analista_senior_2 = models.BooleanField(default=True)
    comercial_analista_senior_3 = models.BooleanField(default=True)
    comercial_analista_senior_4 = models.BooleanField(default=True)
    comercial_analista_senior_5 = models.BooleanField(default=True)
    comercial_analista_senior_6 = models.BooleanField(default=True)
    exportaciones_analista_senior_1 = models.BooleanField(default=True)
    exportaciones_analista_senior_2 = models.BooleanField(default=True)
    exportaciones_analista_senior_3 = models.BooleanField(default=True)
    desarrollo_empresarial_analista_senior_1 = models.BooleanField(default=True)
    administrativo_financiero_analista_senior_1 = models.BooleanField(default=True)
    administrativo_financiero_analista_senior_2 = models.BooleanField(default=True)
    administrativo_financiero_analista_senior_3 = models.BooleanField(default=True)
    administrativo_financiero_analista_senior_4 = models.BooleanField(default=True)
    administrativo_financiero_analista_senior_5 = models.BooleanField(default=True)
    mercadeo_innovacion_analista_senior_1 = models.BooleanField(default=True)
    operaciones_logistica_analista_senior_1 = models.BooleanField(default=True)
    operaciones_logistica_analista_senior_2 = models.BooleanField(default=True)
    operaciones_logistica_analista_senior_3 = models.BooleanField(default=True)
    operaciones_logistica_analista_senior_4 = models.BooleanField(default=True)
    operaciones_logistica_analista_senior_5 = models.BooleanField(default=True)
    comercial_analista_junior_1 = models.BooleanField(default=True)
    comercial_analista_junior_2 = models.BooleanField(default=True)
    comercial_analista_junior_3 = models.BooleanField(default=True)
    comercial_analista_junior_4 = models.BooleanField(default=True)
    comercial_analista_junior_5 = models.BooleanField(default=True)
    comercial_analista_junior_6 = models.BooleanField(default=True)
    comercial_analista_junior_7 = models.BooleanField(default=True)
    comercial_analista_junior_8 = models.BooleanField(default=True)
    exportaciones_analista_junior_1 = models.BooleanField(default=True)
    exportaciones_analista_junior_2 = models.BooleanField(default=True)
    exportaciones_analista_junior_3 = models.BooleanField(default=True)
    exportaciones_analista_junior_4 = models.BooleanField(default=True)
    exportaciones_analista_junior_5 = models.BooleanField(default=True)
    desarrollo_empresarial_analista_junior_1 = models.BooleanField(default=True)
    administrativo_financiero_analista_junior_1 = models.BooleanField(default=True)
    mercadeo_innovacion_analista_junior_1 = models.BooleanField(default=True)
    operaciones_logistica_analista_junior_1 = models.BooleanField(default=True)


class Graficas (models.Model):
    nombre = models.CharField(max_length=45)
    tipo_usuario = models.CharField(max_length=45,default=None)
    grafico = models.CharField(max_length=100)
    nivel = models.IntegerField(default=10)
    tabla = models.CharField(max_length=100,default='',null=True)
    campo = models.CharField(max_length=100,default='',null=True)
    area = models.CharField(max_length=100,default='',null=True)

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
    pcs = models.BooleanField(default=False)
    perfil_pcs = models.ForeignKey(Perfiles_PCS, default=1)





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

class HistorialEmailEnviados(models.Model):
    pedido=models.CharField(max_length=100, null=True)
    empresa=models.CharField(max_length=100, null=True)
    fecha=models.DateField(null=True)
    hora=models.TimeField(null=True)
    tipo = models.CharField(max_length=100, null=True, default=None)
    email = models.CharField(max_length=100, null=True, default=None)


class HistorialEmailReEnviados(models.Model):
    pedido=models.CharField(max_length=100, null=True)
    empresa=models.CharField(max_length=100, null=True)
    fecha=models.DateField(null=True)
    hora=models.TimeField(null=True)
    tipo = models.CharField(max_length=100, null=True, default=None)
    email = models.CharField(max_length=100, null=True, default=None)



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
    ValorFacturaEmitida = models.CharField(max_length=100, null=True)
    FechaPagoFactura = models.DateField(null=True)
    FechaHoy = models.DateField(null=True)
    NumeroFactura = models.CharField(max_length=100, null=True)
    Referencia2 = models.CharField(max_length=100, null=True, default='0')

class FacturasApis(models.Model):
    NombreEmpresa = models.CharField(max_length=100, null=True)
    Identificacion = models.CharField(max_length=100, null=True)
    TipoIdentificacion = models.CharField(max_length=100, null=True)
    Correo = models.CharField(max_length=100, null=True)
    ValorFacturaEmitida = models.CharField(max_length=100, null=True)
    FechaPagoFactura = models.DateField(null=True)
    FechaHoy = models.DateField(null=True)
    NumeroFactura = models.CharField(max_length=100, null=True)
    Referencia2 = models.CharField(max_length=100, null=True,default='0')


class RespuestaOrdenCompraApi(models.Model):
    Identificacion = models.CharField(max_length=100, null=True,default='0000')
    TipoIdentificacion = models.CharField(max_length=100, null=True,default='NIT')
    ValorAprobado = models.CharField(max_length=100, null=True,default='0')
    FechaEmision = models.DateField(null=True,default=datetime.date(1, 1, 1))
    NumeroOrdenCompra = models.CharField(max_length=100, null=True,default='0')
    Interes = models.CharField(max_length=100, null=True,default='0')


class RespuestaFacturaApi(models.Model):
    Identificacion = models.CharField(max_length=100, null=True,default='0000')
    TipoIdentificacion = models.CharField(max_length=100, null=True,default='NIT')
    ValorAprobado = models.CharField(max_length=100, null=True,default='0')
    FechaEmision = models.DateField(null=True,default=datetime.date(1, 1, 1))
    NumeroFactura = models.CharField(max_length=100, null=True,default='0')
    Interes = models.CharField(max_length=100, null=True,default='0')