# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Tipos_radicados(models.Model):
    nombre_tr = models.CharField(max_length=20)
    genera_radicado_salida = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.nombre_tr)

class Tipos_envios (models.Model):
    descripcion = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.descripcion)

class Formas_envios(models.Model):
    tipos_envios = models.ForeignKey(Tipos_envios, default=1)
    nombre_fe = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    genera_planilla = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.nombre_fe)


class Fechas_festivos (models.Model):
    fecha = models.DateField(null=True)

    def __unicode__(self):
        return str(self.fecha)


class Justificacion (models.Model):
    descripcion = models.CharField(max_length=70)

    def __unicode__(self):
        return str(self.descripcion)


class Continentes (models.Model):
    codigo = models.CharField(max_length=2)   # Codigo identificador del Continente no es llave primaria
    descripcion = models.CharField(max_length=45)

    def __unicode__(self):
        return str(self.descripcion)

class Paises (models.Model):
    continentes = models.ForeignKey(Continentes, default=1)
    codigo = models.CharField(max_length=3)  # Codigo identificador del pais no es llave primaria
    descripcion = models.CharField(max_length=45)

    def __unicode__(self):
        return str(self.descripcion)


class Departamentos(models.Model):
    paises = models.ForeignKey(Paises, default=1)
    codigo = models.CharField(max_length=2)  # Codigo identificador del departamento no es llave primaria
    descripcion = models.CharField(max_length=45)

    def __unicode__(self):
        return str(self.descripcion)


class Municipios(models.Model):
    departamentos = models.ForeignKey(Departamentos, default=1)
    codigo = models.CharField(max_length=5)  # Codigo identificador del municipio no es llave primaria
    descripcion = models.CharField(max_length=45)

    def __unicode__(self):
        return str(self.descripcion)


class AreasAtencion(models.Model):
    descripcion = models.CharField(max_length=80)

    def __unicode__(self):
        return str(self.descripcion)


class Peticiones(models.Model):
    descripcion = models.CharField(max_length=80)
    area = models.ForeignKey(AreasAtencion, default=1)

    def __unicode__(self):
        return str(self.descripcion)


class PersonasAtencion(models.Model):
    nombre = models.CharField(max_length=120)
    usuario = models.CharField(max_length=80,null=True)
    telefono = models.CharField(max_length=30)
    email = models.CharField(max_length=80)
    area = models.ForeignKey(AreasAtencion, default=1)

    def __unicode__(self):
        return str(self.descripcion)


class RespuestaPedido(models.Model):
    num_pedido = models.CharField(max_length=80)
    entry_pedido = models.CharField(max_length=80)
    empresa = models.CharField(max_length=80,default=None,null=True)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True,default='01:01:00')
    estado = models.CharField(max_length=80,null=True,default=None)
    respuesta = models.CharField(max_length=80,null=True,default=None)
    email = models.CharField(max_length=80,null=True,default=None)
    peticion = models.ForeignKey(Peticiones, default=1)
    justificacion = models.ForeignKey(Justificacion, default=1)
    justificacion_adicional = models.CharField(max_length=80,null=True,default=None)
    doc_respuesta = models.CharField(max_length=100, null=True,default=None)

    def __unicode__(self):
        return str(self.descripcion)



class LogRespuestaPedido(models.Model):
    num_pedido = models.CharField(max_length=80)
    empresa = models.CharField(max_length=80,default=None,null=True)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True,default='01:01:00')
    email = models.CharField(max_length=80,null=True,default=None)
    accion = models.CharField(max_length=100,null=True,default=None)
    peticion = models.ForeignKey(Peticiones, default=1)

    def __unicode__(self):
        return str(self.descripcion)





class PedidosNovedades(models.Model):
    numero = models.CharField(max_length=20)
    cantidad = models.CharField(max_length=20)
    modificado = models.CharField(max_length=20,default='no')
    nombre = models.CharField(max_length=50)
    peticion=models.ForeignKey(RespuestaPedido, default=1)

    def __unicode__(self):
        return str(self.nombre)


class RespuestaCita(models.Model):
    orden_compra = models.CharField(max_length=80,default='1')
    unidades = models.CharField(max_length=20)
    cajas = models.CharField(max_length=20)
    vehiculo = models.CharField(max_length=20)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    peticion=models.ForeignKey(RespuestaPedido, default=1)

    def __unicode__(self):
        return str(self.unidades)




class Tipos_identificacion(models.Model):
    descripcion = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.descripcion)

class PedidosAlmacenados(models.Model):
    pedido = models.CharField(max_length=40)

    def __unicode__(self):
        return str(self.pedido)


class Empresas(models.Model):
    nombre = models.CharField(max_length=30)
    nit = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    movil = models.CharField(max_length=30)
    responsable = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    continentes = models.ForeignKey(Continentes, default=1)
    paises = models.ForeignKey(Paises, default=1)
    departamentos = models.ForeignKey(Departamentos, default=1)
    municipios = models.ForeignKey(Municipios, default=1)
    edi = models.CharField(max_length=45, null=True, default='1')
    temporada = models.BooleanField(default=False)


    def __unicode__(self):
        return str(self.cargo)

class PedidosOtrosCanales(models.Model):
    num_pedido = models.IntegerField(default=None,primary_key=True)
    empresa = models.ForeignKey(Empresas, default=None,null=True)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True,default='01:01:00')
    estado=models.CharField(max_length=80,null=True,default='en proceso')
    fecha_minima = models.DateField(null=True)
    fecha_maxima = models.DateField(null=True)

    def __unicode__(self):
        return str(self.num_pedido)

class DetallesPedidosOtrosCanales(models.Model):
    num_pedido = models.ForeignKey(PedidosOtrosCanales, default=1)
    cantidad = models.IntegerField(default=1)
    referencia = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100,default='')
    observaciones = models.CharField(max_length=80,null=True)
    empresa = models.ForeignKey(Empresas, default=None,null=True)

    def __unicode__(self):
        return str(self.nombre)


class AsignacionPedidosOtrosCanales(models.Model):
    num_detalle = models.ForeignKey(DetallesPedidosOtrosCanales, default=1)
    cantidad = models.IntegerField(default=1)
    empresa = models.ForeignKey(Empresas, default=None,null=True)

    def __unicode__(self):
        return str(self.nombre)


class ImagenesOtrosCanales(models.Model):
    referencia = models.CharField(max_length=50)
    imagen = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return str(self.referencia)


class Opciones(models.Model):
    descripcion = models.CharField(max_length=20)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.descripcion)

class Atorizaciones(models.Model):
    perfiles = models.ForeignKey(Empresas, default=1)
    opciones = models.ManyToManyField(Opciones)
    descripcion = models.CharField(max_length=20)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.descripcion)






# Tabla soportes papel, electronico y Digital
class Soportes(models.Model):
    descripcion = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.descripcion)

# Tabla Medios de Recepcion  Fisico, Entrega personal, e-mail, etc
class Medios_recepcion(models.Model):
    descripcion = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.descripcion)

# Tabla Tipos de Devoluciones
class Tipos_devoluciones(models.Model):
    descripcion = models.CharField(max_length=40)

    def __unicode__(self):
        return str(self.descripcion)

# Tabla Tipos Anulaciones
class Tipos_anulaciones(models.Model):
    descripcion = models.CharField(max_length=40)

    def __unicode__(self):
        return str(self.descripcion)


# Tabla Terceros
class Terceros (models.Model):
    nombre = models.CharField(max_length=60)
    sigla = models.CharField(max_length=10)
    direccion = models.CharField(max_length=45, null=True)
    telefono = models.CharField(max_length=9999999999999, null=True)
    telefono2 = models.CharField(max_length=9999999999999, null=True)
    celular = models.IntegerField(null=True)
    nit = models.IntegerField(null=True)
    dv = models.CharField(max_length=9, null=True)
    representante_legal = models.CharField(max_length=45, null=True)
    continentes = models.ForeignKey(Continentes, default=1)
    paises = models.ForeignKey(Paises, default=1)
    departamentos = models.ForeignKey(Departamentos, default=1)
    municipios = models.ForeignKey(Municipios, default=1)
    tipo_tercero = models.CharField(max_length=2, null=True)
    email = models.CharField(max_length=45, null=True)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.nombre)

# Tablas para las TRD y TVD
class Series(models.Model):
    codigo = models.CharField(max_length=5)  # Codigo identificador de la serie no es llave primaria
    descripcion = models.CharField(max_length=20)
    observacion = models.CharField(max_length=600)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.descripcion)

class Subseries(models.Model):
    series = models.ForeignKey(Series, default=1)
    codigo = models.CharField(max_length=5)  # Codigo identificador de la Subserie no es llave primaria
    descripcion = models.CharField(max_length=20)
    proceso = models.CharField(max_length=30)
    procedimiento = models.CharField(max_length=30)
    soporte=models.CharField(max_length=30,default=1)
    retencionag = models.IntegerField(null=True)
    retencionac = models.IntegerField(null=True)
    dispocicion_final=models.CharField(max_length=30,default=1)
    observacion = models.CharField(max_length=600)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.descripcion)








class Ubicacion(models.Model):
    codigo = models.CharField(max_length=20)  # Codigo identificador de la ubicacion no es llave primaria
    descripcion = models.CharField(max_length=50)
    continentes = models.ForeignKey(Continentes, default=1)
    paises = models.ForeignKey(Paises, default=1)
    departamentos = models.ForeignKey(Departamentos, default=1)
    municipios = models.ForeignKey(Municipios, default=1)

class Piso(models.Model):
    ubicacion= models.ForeignKey(Ubicacion, default=1)
    numero= models.CharField(max_length=50)

class Salones(models.Model):
    ubicacion= models.ForeignKey(Ubicacion, default=1)
    piso= models.ForeignKey(Piso, default=1)
    salon=models.CharField(max_length=50)

class Estantes(models.Model):
    ubicacion= models.ForeignKey(Ubicacion, default=1)
    piso= models.ForeignKey(Piso, default=1)
    salon=models.ForeignKey(Salones, default=1)
    estante = models.CharField(max_length=50)

class NivelEstantes(models.Model):
    ubicacion= models.ForeignKey(Ubicacion, default=1)
    piso= models.ForeignKey(Piso, default=1)
    salon=models.ForeignKey(Salones, default=1)
    estante=models.ForeignKey(Estantes, default=1)
    nivel = models.CharField(max_length=50)
