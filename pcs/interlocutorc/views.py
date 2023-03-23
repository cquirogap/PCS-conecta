# -*- coding: utf-8 -*-

# Import the datetime module so that we can get the current time
import datetime
import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from interlocutorc.forms import *
from interlocutorc.models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date
from datetime import datetime,timedelta
import requests
import ast
import pytz
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from interlocutorc.serializers import PostSerializer,FacturasSerializer,RespuestaOrdenSerializer,RespuestaFacturaSerializer,MyDataSerializer
import re
from itertools import groupby
# Create your views here.
# This view method handles the request for the root URL /
# See urls.py for the mapping.



class MyListView(APIView):
    def get(self, request,start_date,end_date):
        url = "https://192.168.1.20:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)
        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.20:50000/b1s/v1/SQLQueries('ConsultaPedidosIndicadorJSON')/List?FechaInicial='" + start_date + "'&FechaFinal='" + end_date + "'"

        headers = {
            'Prefer': 'odata.maxpagesize=9999',
            'Cookie': 'B1SESSION=' + respuesta['SessionId']
        }
        response3 = requests.request("GET", url2, headers=headers, verify=False)
        response3 = response3.text
        response3 = response3.replace('null', ' " " ')
        response3 = ast.literal_eval(response3)
        response3 = response3['value']
        response3 = [dict(t) for t in set(tuple(sorted(d.items())) for d in response3)]
        patron = re.compile(r'[^\w\s]+')

        # Iterar sobre cada diccionario de la lista
        for diccionario in response3:
            # Iterar sobre cada clave-valor del diccionario
            for clave, valor in diccionario.items():
                if isinstance(valor, str):
                    diccionario[clave] = patron.sub('', valor)
        lista=[]
        for d in response3:
            if d['U_EAN']==' ':
                Eandependencia=d['EANEntrega']
                NombreDep=d['SitioEntrega']
            else:
                Eandependencia=d['U_EAN']
                NombreDep = d['NombreDep']
            if d['U_HBT1_TIPO_ORD_EDI']=='220':
                Tipopedido='Almacenamiento'
            elif d['U_HBT1_TIPO_ORD_EDI']=='YB1':
                Tipopedido = 'Predistribuido'
            elif d['U_HBT1_TIPO_ORD_EDI']=='YA9':
                Tipopedido = 'Consolidado'
            else:
                Tipopedido='Sin Asignar'

            lista_individual={
                'OrdenEDI': d['OrdenEDI'],
                'OrdenSAP':d['PedidoVta'],
                'Cliente':d['Cliente'],
                'Empresario':d['Empresario'],
                'NombreCliente':d['NombreCliente'],
                'NombreEmpresario':d['NombreEmpresario'],
                'GLNEntrega':d['EANEntrega'],
                'SitioEntrega':d['SitioEntrega'],
                'FechaExpedicionEDI':d['FechaDocto'],
                'FechaMinimaEdi':d['FechaMinEnt'],
                'FechaMaximaEdi':d['FechaMaxEnt'],
                'GLNCod_Dep':Eandependencia,
                'NombreDep':NombreDep,
                'EANproducto':d['EANArticulo'],
                'DescripArticulo':d['DescripArticulo'],
                'Cantidad':d['CantidadFactura'],
                'ValorUnitario':d['PrecioPed'],
                'ValorTotal':d['TotalPed'],
                'SKU / REFERENCIA CLIENTE':d['PLU'],
                'SKU / REFERENCIA EMPRESARIO':d['CodArticulo'],
                'GLNCliente':d['Cliente'],
                'Tipopedido':Tipopedido
            }
            lista.append(lista_individual)


        response3=lista
        lista_ordenada = sorted(response3, key=lambda x: (x['OrdenEDI'], x['OrdenSAP'], x['Cliente'], x['Empresario'],x['NombreCliente'],x['NombreEmpresario'],x['GLNEntrega'],x['SitioEntrega'],x['FechaExpedicionEDI'],x['FechaMinimaEdi'],x['FechaMaximaEdi'],x['GLNCod_Dep'],x['NombreDep'],x['GLNCliente'],x['Tipopedido']))

        grupos_ordenados = groupby(lista_ordenada, key=lambda x: (x['OrdenEDI'], x['OrdenSAP'], x['Cliente'], x['Empresario'],x['NombreCliente'],x['NombreEmpresario'],x['GLNEntrega'],x['SitioEntrega'],x['FechaExpedicionEDI'],x['FechaMinimaEdi'],x['FechaMaximaEdi'],x['GLNCod_Dep'],x['NombreDep'],x['GLNCliente'],x['Tipopedido']))

        resultado = [{'OrdenEDI': OrdenEDI, 'OrdenSAP': OrdenSAP, 'Cliente': Cliente, 'Empresario': Empresario, 'NombreCliente': NombreCliente, 'NombreEmpresario': NombreEmpresario, 'GLNEntrega': GLNEntrega, 'SitioEntrega': SitioEntrega, 'FechaExpedicionEDI': FechaExpedicionEDI, 'FechaMinimaEdi': FechaMinimaEdi,
                      'FechaMaximaEdi': FechaMaximaEdi,'GLNCod_Dep': GLNCod_Dep,'NombreDep': NombreDep,'GLNCliente': GLNCliente,'Tipopedido': Tipopedido, 'lineas_orden': list(info)} for
                     (OrdenEDI, OrdenSAP, Cliente, Empresario, NombreCliente, NombreEmpresario, GLNEntrega, SitioEntrega, FechaExpedicionEDI, FechaMinimaEdi, FechaMaximaEdi, GLNCod_Dep, NombreDep, GLNCliente, Tipopedido),
                     info in grupos_ordenados]

        serializer = MyDataSerializer(resultado, many=True)
        return Response(serializer.data)


class ApiPrueba(ModelViewSet):
    serializer_class = PostSerializer
    now = datetime.now(pytz.timezone('America/Bogota'))
    hoy = now.date()
    objetos_a = ClientesApi.objects.filter(FechaEntrega__gte=hoy)
    ids_b = RespuestaOrdenCompraApi.objects.values_list('NumeroOrdenCompra', flat=True)
    queryset = [objeto for objeto in objetos_a if objeto.NumeroPedido not in ids_b]

class ApiFacturas(ModelViewSet):
    serializer_class = FacturasSerializer
    now = datetime.now(pytz.timezone('America/Bogota'))
    hoy = now.date()
    objetos_a = FacturasApi.objects.filter(FechaPagoFactura__gte=hoy)
    ids_b = RespuestaFacturaApi.objects.values_list('NumeroFactura', flat=True)
    queryset = [objeto for objeto in objetos_a if objeto.NumeroFactura not in ids_b]

class RespuestaOrdenApi(ModelViewSet):
    serializer_class = RespuestaOrdenSerializer
    now = datetime.now(pytz.timezone('America/Bogota'))
    hoy = now.date()
    queryset = RespuestaOrdenCompraApi.objects.all()

class RespuestaFacturaApi(ModelViewSet):
    serializer_class = RespuestaFacturaSerializer
    now = datetime.now(pytz.timezone('America/Bogota'))
    hoy = now.date()
    queryset = RespuestaFacturaApi.objects.all()

def admin_admin(request):

    if request.method == 'GET':
        current_user = request.user
        permisos = Permisos.objects.filter(usuario_id=current_user.id).first()
        lista_admin = User.objects.all()

        if not current_user.is_staff:
            return HttpResponseRedirect('/login/')

        if permisos.administrador == False :
            messages.add_message(request, messages.ERROR,'No tienes permitido el acceso a ese modulo')
            return HttpResponseRedirect('/administracion/')

        return render(request, "admin_admin.html", {'user_name': current_user.first_name,
                                                    'lista_admin': lista_admin,
                                                    'permisos': permisos})
    else:
        pass

def admin_registrar(request):

    if request.method == 'GET':
        current_user = request.user
        permisos = Permisos.objects.filter(usuario_id=current_user.id).first()

        if not current_user.is_staff:
            return HttpResponseRedirect('/login/')

        if permisos.administrador == False:
            messages.add_message(request, messages.ERROR, 'No tienes permitido el acceso a ese modulo')
            return HttpResponseRedirect('/administracion/')

        return render(request, "admin_admin_registrar.html", {'user_name': current_user.first_name, 'permisos': permisos})
    else:
        pass

def definir_login(request):
    # Define  si al   login redirecciona  a os eventos  o  a la pagina de adminsitracion
    # de  acuerdo al la variable is_staff del  modeloo  user
    usuario_actual = request.user
    if usuario_actual.is_staff:
        return HttpResponseRedirect('/administracion/')
    else:
        return HttpResponseRedirect('/login/')


def panel_administracion(request):
    # Render  administracion.html
    usuario_actual = request.user
    if not usuario_actual.is_staff:
        return HttpResponseRedirect('/login/')

    if request.method == 'GET':
        hoy=datetime.now()
        current_user = request.user
        permisos = Permisos.objects.filter(usuario_id=current_user.id).first()
        usuario_datos = Usuarios_datos.objects.filter(usuario_id=current_user.id).first()
        historial = HistoriaUsuario(
            usuario_id=int(current_user.id),
            empresa_id=int(usuario_datos.empresa_id),
            accion='Logueo de Usuario',
            fecha=hoy,
        )
        historial.save()
        return render(request, "administracion.html", {'user': usuario_actual, 'permisos': permisos,'permiso_usuario': usuario_datos})
    else:
        pass

def panel_ayuda(request):
    # Render  administracion.html
    if request.method == 'GET':
        current_user = request.user
        usuario_datos = Usuarios_datos.objects.filter(usuario_id=current_user.id).first()
        return render(request, "ayuda.html", {'permiso_usuario': usuario_datos
                                                        })
    else:
        pass

def tarea_api():
    try:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Inicio de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.20:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.20:50000/b1s/v1/SQLQueries('ConsultaPedidosApi')/List?FechaHoy='" + str(hoy) + "'"

        headers = {
            'Prefer': 'odata.maxpagesize=999999',
            'Cookie': 'B1SESSION=' + respuesta['SessionId']
        }
        response = requests.request("GET", url2, headers=headers, verify=False)
        response = response.text
        response = response.replace('null', ' " " ')
        response = ast.literal_eval(response)
        response = response['value']
        for datos in response:
            if Empresas.objects.filter(nombre=str(datos['CardName'])).exists():
                try:
                    pedido_almacenado = ClientesApi.objects.get(NumeroPedido=datos['DocNum'])
                    pass
                except:
                    fecha_pedido=str(datos['DocDueDate'])
                    fecha_pedido = datetime.strptime(fecha_pedido, '%Y%m%d')
                    fecha_hoy = str(datos['DocDate'])
                    fecha_hoy = datetime.strptime(fecha_hoy, '%Y%m%d')
                    nuevo_pedido = ClientesApi(
                        NombreEmpresa=datos['CardName'],
                        Identificacion=datos['LicTradNum'],
                        TipoIdentificacion='NIT',
                        Correo=datos['E_Mail'],
                        ValorOrden=datos['DocTotal'],
                        FechaEntrega=fecha_pedido,
                        FechaPago=fecha_pedido,
                        FechaHoy=fecha_hoy,
                        NumeroPedido=datos['DocNum'],
                    )
                    nuevo_pedido.save()
            else:
                pass

        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
    except:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Error de conexion',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()


def facturas_api():
    try:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Inicio de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.20:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.20:50000/b1s/v1/SQLQueries('ConsultasFacturasApi')/List"

        headers = {
            'Prefer': 'odata.maxpagesize=999999',
            'Cookie': 'B1SESSION=' + respuesta['SessionId']
        }
        response = requests.request("GET", url2, headers=headers, verify=False)
        response = response.text
        response = response.replace('null', ' " " ')
        response = ast.literal_eval(response)
        response = response['value']
        for datos in response:
            if Empresas.objects.filter(nombre=str(datos['CardName'])).exists():
                try:
                    pedido_almacenado = FacturasApi.objects.get(NumeroFactura=datos['DocNum'])
                    pass
                except:
                    fecha_pedido=str(datos['DocDueDate'])
                    fecha_pedido = datetime.strptime(fecha_pedido, '%Y%m%d')
                    fecha_hoy = str(datos['DocDate'])
                    fecha_hoy = datetime.strptime(fecha_hoy, '%Y%m%d')
                    nuevo_factura = FacturasApi(
                        NombreEmpresa=datos['CardName'],
                        Identificacion=datos['LicTradNum'],
                        TipoIdentificacion='NIT',
                        Correo=datos['E_Mail'],
                        ValorFacturaEmitida=datos['DocTotal'],
                        FechaPagoFactura=fecha_pedido,
                        FechaHoy=fecha_hoy,
                        NumeroFactura=datos['DocNum'],
                    )
                    nuevo_factura.save()
            else:
                pass

        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
    except:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Error de conexion',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()


def prueba(request):
    email = EmailMessage('TIENES UN NUEVO PEDIDO',
                         'hssg',
                         to=['juan   sebastianduartes@gmail.com'])
    email.send()


def tarea_correo_pedido():
    try:
        estado = 'bost_Open'
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy=now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Inicio de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.20:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.20:50000/b1s/v1/PurchaseOrders?$orderby=DocDate desc&$select=DocNum,DocEntry,CardCode,CardName&$filter=DocDate eq '" \
               + str(hoy) + "'"

        headers = {
            'Prefer': 'odata.maxpagesize=999999',
            'Cookie': 'B1SESSION=' + respuesta['SessionId']
        }
        response = requests.request("GET", url2, headers=headers, verify=False)
        response = ast.literal_eval(response.text)
        response = response['value']
        for datos in response:
            if Empresas.objects.filter(nombre=str(datos['CardName'])).exists():
                try:
                    pedido_almacenado = PedidosAlmacenados.objects.get(pedido=datos['DocNum'])
                    pass
                except:
                    try:
                        dependencias = 'LOGISTICA Y DESPACHOS'
                        url3 = "https://192.168.1.20:50000/b1s/v1/SQLQueries('ConsultaEmailEmpresa')/List?empresa='" + \
                               datos['CardCode'] + "'&dependencia='" + dependencias + "'"
                        response2 = requests.request("GET", url3, headers=headers, verify=False)
                        response2 = ast.literal_eval(response2.text)
                        response2 = response2['value']
                        if response2==[]:
                            errores = HistorialErrorTarea(
                                accion='No se tiene correo asignado al titulo LOGISTICA Y DESPACHOS',
                                fecha=hoy,
                                hora=hora,
                                empresa=str(datos['CardName']),
                                pedido=str(datos['DocNum'])
                            )
                            errores.save()
                        else:
                            response2 = response2[0]
                            response2 = response2['E_MailL']
                            response2 = str(response2).split(";")
                            for correos in response2:
                                correos=correos.lstrip()
                                expresion_regular = r"(?i)(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
                                valido = re.match(expresion_regular, correos) is not None
                                if valido == True:
                                    try:
                                        email = EmailMessage('TIENES UN NUEVO PEDIDO '+str(datos['DocNum']),
                                                             'Ha recibido un pedido nuevo.Para conocer el detalle del pedido ingresa al siguiente link '
                                                             + 'http://45.56.118.44/configuracion/solicitud_pedido_orden/detalle/' + str(
                                                                 datos['DocEntry']) + '/',
                                                             to=[correos])
                                        email.send()
                                        enviados = HistorialEmailEnviados(
                                            fecha=hoy,
                                            hora=hora,
                                            empresa=str(datos['CardName']),
                                            pedido=str(datos['DocNum']),
                                            tipo='enviado',
                                            email=correos
                                        )
                                        enviados.save()
                                    except:
                                        now = datetime.now(pytz.timezone('America/Bogota'))
                                        hoy = now.date()
                                        hora = now.time()
                                        errores = HistorialErrorTarea(
                                            accion='Fallo al enviar al correo' + str(correos),
                                            fecha=hoy,
                                            hora=hora,
                                            empresa=str(datos['CardName']),
                                            pedido=str(datos['DocNum'])
                                        )
                                        errores.save()
                                elif valido == False:
                                    now = datetime.now(pytz.timezone('America/Bogota'))
                                    hoy = now.date()
                                    hora = now.time()
                                    errores = HistorialErrorTarea(
                                        accion='No se reconoce el correo ' + str(correos),
                                        fecha=hoy,
                                        hora=hora,
                                        empresa=str(datos['CardName']),
                                        pedido=str(datos['DocNum'])
                                    )
                                    errores.save()
                            pedido_al = PedidosAlmacenados(
                                pedido=datos['DocNum']
                            )
                            pedido_al.save()
                    except:
                        now = datetime.now(pytz.timezone('America/Bogota'))
                        hoy = now.date()
                        hora = now.time()
                        errores = HistorialErrorTarea(
                            accion='No se envio el correo',
                            fecha=hoy,
                            hora=hora,
                            empresa=str(datos['CardName']),
                            pedido=str(datos['DocNum'])
                        )
                        errores.save()
            else:
                enviados = HistorialEmailEnviados(
                    fecha=hoy,
                    hora=hora,
                    empresa=str(datos['CardName']),
                    pedido=str(datos['DocNum']),
                    tipo='noregistrado',
                    email=None
                )
                enviados.save()

        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
    except:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Error de conexion',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()