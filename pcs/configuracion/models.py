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

class Tipos_identificacion(models.Model):
    descripcion = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.descripcion)

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


    def __unicode__(self):
        return str(self.cargo)

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

class Dependencias(models.Model):
    codigo = models.CharField(max_length=8, primary_key=True, default=1)
    codigopadre = models.CharField(max_length=8) # Codigo dependencia no es llave primaria
    codigoterritorio = models.CharField(max_length=8)  # Codigo dependencia no es llave primaria
    sigla = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=30)
    estado = models.BooleanField(default=True)
    continentes = models.ForeignKey(Continentes, default=1)
    paises = models.ForeignKey(Paises, default=1)
    departamentos = models.ForeignKey(Departamentos, default=1)
    municipios = models.ForeignKey(Municipios, default=1)
    direccion = models.CharField(max_length=50)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)


    def __unicode__(self):
        return str(self.descripcion)

class Dependencias_visibles(models.Model):
    dependencias = models.ForeignKey(Dependencias, default=1)

    def __unicode__(self):
        return str(self.dependencias)

class Consecutivos(models.Model):
    codigo = models.CharField(max_length=200, primary_key=True, default=1)
    ano = models.IntegerField(null=True)
    dependencias = models.ForeignKey(Dependencias,null=True)
    secuencia = models.CharField(null=True,max_length=6)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)
    tipo= models.CharField(max_length=50,default=1)
    usuario_origen=models.ForeignKey(User,null=True)
    accion=models.CharField(null=True,max_length=30)

    def __unicode__(self):
        return str(self.codigo)

class Anos(models.Model):
    ano = models.IntegerField(null=True)

class CarpetaAno(models.Model):
    ano=models.ForeignKey(Anos,null=True)
    dependencias = models.ForeignKey(Dependencias,null=True)
    usuario_origen=models.ForeignKey(User,null=True)
    accion=models.CharField(null=True,max_length=50)



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

class Tipos_documentos(models.Model):
    dependencias = models.ForeignKey(Dependencias, default=1)
    tipos_radicados = models.ForeignKey(Tipos_radicados, default=1)
    descripcion = models.CharField(max_length=40)
    dias_tramite = models.IntegerField(null=True)
    publicar = models.BooleanField(default=True)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

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

class Matriz(models.Model):
    dependencia = models.ForeignKey(Dependencias,default=1)
    serie = models.ForeignKey(Series,default=1)
    subserie = models.ForeignKey(Subseries,default=1)
    soporte=models.CharField(max_length=30)
    tipos_documentos=models.ForeignKey(Tipos_documentos,default=1)
    estado=models.CharField(max_length=30,default='activo')

class Trd(models.Model):
    codigo = models.CharField(max_length=5)  # Codigo identificador de la TRD no es llave primaria
    version = models.IntegerField(null=True)
    administrativa = models.ForeignKey(Dependencias, related_name='administrativa')
    productora = models.ForeignKey(Dependencias, related_name='productora')
    series = models.ForeignKey(Series, default=1)
    subseries = models.ForeignKey(Subseries, default=1)
    descripcion = models.CharField(max_length=20)
    acta = models.CharField(max_length=40)
    fechaaprobacion = models.DateField(null=True)
    observacion = models.CharField(max_length=600)
    creado = models.DateTimeField(null=True)
    modificado = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.descripcion)

class Trd_tiposdocumentos(models.Model):
    trd = models.ForeignKey(Trd, default=1)
    descripcion = models.CharField(max_length=20)

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
