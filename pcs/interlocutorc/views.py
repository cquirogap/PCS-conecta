# -*- coding: utf-8 -*-

# Import the datetime module so that we can get the current time
import datetime
import json

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from interlocutorc.forms import *
from interlocutorc.models import *
from configuracion.models import *
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import date
from datetime import datetime,timedelta
import requests
import ast
import pytz
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from interlocutorc.serializers import PostSerializer,FacturasSerializer,RespuestaOrdenSerializer,RespuestaFacturaSerializer,MyDataSerializer,RespuestaOrdenesSerializer
import re
from itertools import groupby
from django.contrib.auth.views import LoginView
import sys

# Create your views here.
# This view method handles the request for the root URL /
# See urls.py for the mapping.


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'



class MyListView(APIView):
    def get(self, request,start_date,end_date):
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)
        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaPedidosIndicadorJSON')/List?FechaInicial='" + start_date + "'&FechaFinal='" + end_date + "'"

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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
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
    hoy = hoy + timedelta(days=10)	
    objetos_a = FacturasApi.objects.filter(FechaPagoFactura__gte=hoy)
    ids_b = RespuestaFacturaApi.objects.values_list('NumeroFactura', flat=True)
    queryset = [objeto for objeto in objetos_a if objeto.NumeroFactura not in ids_b]

class RespuestaOrdenApi(ModelViewSet):
    serializer_class = RespuestaOrdenSerializer
    now = datetime.now(pytz.timezone('America/Bogota'))
    hoy = now.date()
    queryset = RespuestaOrdenCompraApi.objects.all()

class RespuestaOrdenesApi(ModelViewSet):
    queryset = RespuestaOrdenCompraApis.objects.all()
    serializer_class = RespuestaOrdenesSerializer





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




def pruebacorreos():
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
            tipo='crediya',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaPedidosApis1')/List?FechaHoy='" + str(hoy) + "'"

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
                        ValorOrden=format(int(datos['DocTotal']) - int(datos['VatSum']), '0,.0f'),
                        FechaEntrega=fecha_pedido,
                        FechaPago=fecha_pedido,
                        FechaHoy=fecha_hoy,
                        NumeroPedido=datos['DocNum'],
                    )
                    try:
                        nuevo_pedido.save()
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al registrar el pedido',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='crediya',
                        )
                        errores.save()
                        pass
                    try:
                        intereses_minimo = 20000
                        intereses_segundo = 40000
                        valor_total=int(datos['DocTotal']) - int(datos['VatSum'])
                        medio=valor_total/2
                        interes = 0.018 * medio
                        if intereses_minimo > interes:
                            interes = intereses_minimo
                        elif intereses_segundo > interes:
                            interes = intereses_segundo
                        desembolso = medio - interes
                        desembolso = "{:,.0f}".format(desembolso)
                        interes = "{:,.0f}".format(interes)
                        html_content = render_to_string('basecorreropedidos.html', {
                            'numero_orden': datos['DocNum'],
                            'nombre_empresa': datos['CardName'],
                            'intereses': interes,
                            'tasa_interes': '1.8%MA',
                            'valor_desembolso': desembolso,
                        })
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al calcular valores',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='crediya',
                        )
                        errores.save()
                        pass

                    # Crear el correo electrónico
                    subject = 'Aviso de Servicio Financiero '+str(datos['DocNum'])
                    from_email = 'conectaportalweb@gmail.com'
                    to = [datos['E_Mail']]  # Lista de destinatarios
                    text_content = 'Este es un correo electronico con formato HTML.'

                    # Configurar el correo electrónico con formato alternativo (HTML)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                    msg.attach_alternative(html_content, "text/html")

                    # Enviar el correo electrónico
                    try:
                        msg.send()
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al enviar el correo',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='crediya',
                        )
                        errores.save()
                        pass
            else:
                pass
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
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
                tipo='crediya',
            )
        errores.save()






def pruebacorreosfactura():
    try:
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        hoy_filtro = date.today()
        hoy_filtro = hoy_filtro + timedelta(days=10)
        hoy_filtro = hoy_filtro.strftime("%Y-%m-%d")
        errores = HistorialErrorApi(
            accion='Inicio de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
            tipo='credilisto',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultasFacturasApis3')/List?fecha='" + hoy_filtro +"'"

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
                        Referencia2=datos['NumAtCard'],
                    )
                    try:
                        nuevo_factura.save()
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al registrar la factura',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='credilisto',
                        )
                        errores.save()
                        pass
                    try:
                        fecha_pedido=fecha_pedido.date()
                        diferencia = (fecha_pedido - hoy).days
                        intereses_minimo = 20000
                        intereses_segundo = 40000
                        valor_total = int(datos['DocTotal'])
                        medio = valor_total*0.8
                        interes=diferencia*0.000533333*medio
                        if intereses_minimo > interes:
                            interes = intereses_minimo
                        elif intereses_segundo > interes:
                            interes= intereses_segundo
                        desembolso = medio - interes
                        desembolso = "{:,.0f}".format(desembolso)
                        interes = "{:,.0f}".format(interes)
                        html_content = render_to_string('basecorrerofactura.html', {
                            'numero_orden': datos['DocNum'],
                            'nombre_empresa': datos['CardName'],
                            'intereses': interes,
                            'tasa_interes': '1.6%MA',
                            'diferencia': diferencia,
                            'valor_desembolso': desembolso,
                            'referencia': datos['NumAtCard'],
                        })
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al calcular valores',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='credilisto',
                        )
                        errores.save()
                        pass

                    # Crear el correo electrónico
                    subject = 'Aviso de Servicio Financiero CrediListo ' + str(datos['DocNum'])
                    from_email = 'conectaportalweb@gmail.com'
                    to = [datos['E_Mail']]  # Lista de destinatarios
                    text_content = 'Este es un correo electronico con formato HTML.'

                    # Configurar el correo electrónico con formato alternativo (HTML)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                    msg.attach_alternative(html_content, "text/html")

                    # Enviar el correo electrónico
                    try:
                        msg.send()
                    except:
                        errores = HistorialErrorApi(
                            accion='Error al enviar el correo',
                            fecha=hoy,
                            hora=hora,
                            empresa=datos['CardName'],
                            pedido=datos['DocNum'],
                            tipo='credilisto',
                        )
                        errores.save()
                        pass
            else:
                pass

        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
            tipo='credilisto',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)

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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)



def pruebasap(request):
    # URL para autenticarse y obtener el SessionId
    url = "https://192.168.1.2:50000/b1s/v1/Login"

    payload = "{\"CompanyDB\":\"PCS19012024\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

    response = requests.request("POST", url, data=payload, verify=False)

    respuesta = ast.literal_eval(response.text)

    url = "https://192.168.1.2:50000/b1s/v1/VendorPayments"

    payload = json.dumps({
        "DocNum": 41058,
        "DocType": "rSupplier",
        "HandWritten": "tNO",
        "Printed": "tYES",
        "DocDate": "2024-03-21T00:00:00Z",
        "CardCode": "P005367",
        "CardName": "PISCU S.A.S",
        "Address": "CR 48 A 80 13 000000  MEDELLIN COLOMBIA",
        "CashAccount": None,
        "DocCurrency": "$",
        "CashSum": 0,
        "CheckAccount": None,
        "TransferAccount": "11100502",
        "TransferSum": 6110010,
        "TransferDate": "2024-03-21T00:00:00Z",
        "TransferReference": None,
        "LocalCurrency": "tNO",
        "DocRate": 0,
        "Reference1": "3",
        "Reference2": None,
        "CounterReference": None,
        "Remarks": "esto es una prueba",
        "JournalRemarks": "Cancelado",
        "SplitTransaction": "tNO",
        "ContactPersonCode": 10308,
        "ApplyVAT": "tNO",
        "TaxDate": "2024-03-21T00:00:00Z",
        "BankCode": None,
        "BankAccount": None,
        "DiscountPercent": 0,
        "ProjectCode": None,
        "CurrencyIsLocal": "tNO",
        "DeductionPercent": 0,
        "DeductionSum": 0,
        "CashSumFC": 0,
        "CashSumSys": 0,
        "BoeAccount": None,
        "BillOfExchangeAmount": 0,
        "BillofExchangeStatus": None,
        "BillOfExchangeAmountFC": 0,
        "BillOfExchangeAmountSC": 0,
        "BillOfExchangeAgent": None,
        "WTCode": None,
        "WTAmount": 0,
        "WTAmountFC": 0,
        "WTAmountSC": 0,
        "WTAccount": None,
        "WTTaxableAmount": 0,
        "Proforma": "tNO",
        "PayToBankCode": None,
        "PayToBankBranch": None,
        "PayToBankAccountNo": None,
        "PayToCode": "PRINCIPAL",
        "PayToBankCountry": None,
        "IsPayToBank": "tNO",
        "DocEntry": 3,
        "PaymentPriority": "bopp_Priority_6",
        "TaxGroup": None,
        "BankChargeAmount": 0,
        "BankChargeAmountInFC": 0,
        "BankChargeAmountInSC": 0,
        "UnderOverpaymentdifference": 0,
        "UnderOverpaymentdiffSC": 0,
        "WtBaseSum": 0,
        "WtBaseSumFC": 0,
        "WtBaseSumSC": 0,
        "VatDate": "2024-03-21T00:00:00Z",
        "TransactionCode": "",
        "PaymentType": "bopt_None",
        "TransferRealAmount": 0,
        "DocObjectCode": "bopot_OutgoingPayments",
        "DocTypte": "rSupplier",
        "DueDate": "2024-03-21T00:00:00Z",
        "LocationCode": None,
        "Cancelled": "tYES",
        "ControlAccount": "23359525",
        "UnderOverpaymentdiffFC": 0,
        "AuthorizationStatus": "pasWithout",
        "BPLID": None,
        "BPLName": None,
        "VATRegNum": None,
        "BlanketAgreement": None,
        "PaymentByWTCertif": "tNO",
        "Cig": None,
        "Cup": None,
        "AttachmentEntry": None,
        "SignatureInputMessage": None,
        "SignatureDigest": None,
        "CertificationNumber": None,
        "PrivateKeyVersion": None,
        "U_HBT_AreVal": "Comun",
        "U_HBT_Tercero": None,
        "U_GSP_TPVREF": None,
        "U_GSP_TPVLINE": None,
        "U_GSP_TPVPAYMETHOD": None,
        "U_HBT1_CPTO": "Pago",
        "U_HBT_PagoAnticipo": "N",
        "U_BP_Confd": "N",
        "U_BP_DocNr": None,
        "U_BP_Seque": None,
        "PaymentChecks": [],
        "PaymentInvoices": [],
        "PaymentCreditCards": [],
        "PaymentAccounts": [],
        "PaymentDocumentReferencesCollection": [],
        "BillOfExchange": {},
        "WithholdingTaxCertificatesCollection": [],
        "ElectronicProtocols": [],
        "CashFlowAssignments": [],
        "Payments_ApprovalRequests": [],
        "WithholdingTaxDataWTXCollection": []
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'B1SESSION=746b4846-e7b4-11ee-c000-000c2986aa05-140529280101248-4921; ROUTEID=.node4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def prubasap2(request):
    url = "https://192.168.1.2:50000/b1s/v1/Login"

    payload = "{\"CompanyDB\":\"PRUEBALOC04042025\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

    response = requests.request("POST", url, data=payload, verify=False)

    respuesta = ast.literal_eval(response.text)
    # URL del endpoint de VendorPayments
    url_pagos_efectuados = "https://192.168.1.2:50000/b1s/v1/VendorPayments"

    # Datos del nuevo pago efectuado que quieres enviar
    nuevo_pago_efectuado = {
        "DocNum": 51656,
        "DocType": "rSupplier",
        "HandWritten": "tNO",
        "Printed": "tNO",
        "DocDate": "2025-04-07T00:00:00Z",
        "CardCode": "P004269",
        "CardName": "COMERCIALIZADORA DE PRODUCTOS WET CO SAS",
        "Address": "CL 19 B 35 71\r000000  BOGOTA\rCOLOMBIA",
        "CashAccount": "42100517",
        "DocCurrency": "$",
        "CashSum": 40000.0,
        "CheckAccount": None,
        "TransferAccount": "11201005",
        "TransferSum": 132983.0,
        "TransferDate": "2025-04-07T00:00:00Z",
        "TransferReference": None,
        "LocalCurrency": "tNO",
        "DocRate": 0.0,
        "Reference1": "51656",
        "Reference2": None,
        "CounterReference": None,
        "Remarks": None,
        "JournalRemarks": "ANTICIPO 0C 155434",
        "SplitTransaction": "tNO",
        "ContactPersonCode": 12354,
        "ApplyVAT": "tNO",
        "TaxDate": "2025-04-07T00:00:00Z",
        "Series": 119,
        "BankCode": None,
        "BankAccount": None,
        "DiscountPercent": 0.0,
        "ProjectCode": None,
        "CurrencyIsLocal": "tNO",
        "DeductionPercent": 0.0,
        "DeductionSum": 0.0,
        "CashSumFC": 0.0,
        "CashSumSys": 9.68,
        "BoeAccount": None,
        "BillOfExchangeAmount": 0.0,
        "BillofExchangeStatus": None,
        "BillOfExchangeAmountFC": 0.0,
        "BillOfExchangeAmountSC": 0.0,
        "BillOfExchangeAgent": None,
        "WTCode": None,
        "WTAmount": 0.0,
        "WTAmountFC": 0.0,
        "WTAmountSC": 0.0,
        "WTAccount": None,
        "WTTaxableAmount": 0.0,
        "Proforma": "tNO",
        "PayToBankCode": None,
        "PayToBankBranch": None,
        "PayToBankAccountNo": None,
        "PayToCode": "PRINCIPAL",
        "PayToBankCountry": None,
        "IsPayToBank": "tNO",
        "DocEntry": 800056499,
        "PaymentPriority": "bopp_Priority_6",
        "TaxGroup": None,
        "BankChargeAmount": 0.0,
        "BankChargeAmountInFC": 0.0,
        "BankChargeAmountInSC": 0.0,
        "UnderOverpaymentdifference": 0.0,
        "UnderOverpaymentdiffSC": 0.0,
        "WtBaseSum": 0.0,
        "WtBaseSumFC": 0.0,
        "WtBaseSumSC": 0.0,
        "VatDate": "2025-04-07T00:00:00Z",
        "TransactionCode": "",
        "PaymentType": "bopt_None",
        "TransferRealAmount": 0.0,
        "DocObjectCode": "bopot_OutgoingPayments",
        "DocTypte": "rSupplier",
        "DueDate": "2025-04-07T00:00:00Z",
        "LocationCode": None,
        "Cancelled": "tNO",
        "ControlAccount": "13300612",
        "UnderOverpaymentdiffFC": 0.0,
        "AuthorizationStatus": "pasWithout",
        "BPLID": None,
        "BPLName": None,
        "VATRegNum": None,
        "BlanketAgreement": None,
        "PaymentByWTCertif": "tNO",
        "Cig": None,
        "Cup": None,
        "AttachmentEntry": None,
        "SignatureInputMessage": None,
        "SignatureDigest": None,
        "CertificationNumber": None,
        "PrivateKeyVersion": None,
        "EDocExportFormat": None,
        "ElecCommStatus": None,
        "ElecCommMessage": None,
        "SplitVendorCreditRow": "tNO",
        "DigitalPayments": "tNO",
        "U_HBT_AreVal": "Comun",
        "U_HBT_Tercero": None,
        "U_GSP_TPVREF": None,
        "U_GSP_TPVLINE": None,
        "U_GSP_TPVPAYMETHOD": None,
        "U_HBT1_CPTO": "Pago",
        "U_HBT_PagoAnticipo": "N",
        "U_BP_Confd": "N",
        "U_BP_DocNr": None,
        "U_BP_Seque": None,
        "PaymentChecks": [],
        "PaymentInvoices": [
            {
                "LineNum": 0,
                "DocEntry": 152282,
                "SumApplied": -10000.0,
                "AppliedFC": 0.0,
                "AppliedSys": 103.5,
                "DocRate": 0.0,
                "DocLine": 0,
                "InvoiceType": "it_PurchaseCreditNote",
                "PaidSum": 0.0,
                "InstallmentId": 1,
                "WitholdingTaxApplied": 0.0,
                "WitholdingTaxAppliedFC": 0.0,
                "WitholdingTaxAppliedSC": 0.0,
                "LinkDate": None,
                "DistributionRule": None,
                "DistributionRule2": None,
                "DistributionRule3": None,
                "DistributionRule4": None,
                "DistributionRule5": None,
                "TotalDiscount": -100,
            }
        ],
        "PaymentCreditCards": [],
        "PaymentAccounts": [],
        "PaymentDocumentReferencesCollection": [],
        "BillOfExchange": {},
        "WithholdingTaxCertificatesCollection": [],
        "ElectronicProtocols": [],
        "CashFlowAssignments": [],
        "Payments_ApprovalRequests": [],
        "WithholdingTaxDataWTXCollection": []






    }

    # Convierte los datos a formato JSON
    payload_pagos_efectuados = json.dumps(nuevo_pago_efectuado)

    # Encabezados de la solicitud HTTP
    headers_pagos_efectuados = {
        'Content-Type': 'application/json',
        # Agrega aquí tu cookie de sesión
        'Cookie': 'B1SESSION=' + respuesta['SessionId']
    }

    # Realiza la solicitud POST al Service Layer para crear un nuevo pago efectuado
    response_pagos_efectuados = requests.post(url_pagos_efectuados, headers=headers_pagos_efectuados,
                                              data=payload_pagos_efectuados, verify=False)

    # Verifica el estado de la respuesta
    if response_pagos_efectuados.status_code == 201:
        print("Pago efectuado creado exitosamente.")
    else:
        print("Error al crear el pago efectuado:", response_pagos_efectuados.text)


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
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaPedidosApis')/List?FechaHoy='" + str(hoy) + "'"

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
                        ValorOrden=format(int(datos['DocTotal']) - int(datos['VatSum']), '0,.0f'),
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
        errores = HistorialErrorApi(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)


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
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultasFacturasApis')/List"

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
                        Referencia2=datos['NumAtCard'],
                    )
                    nuevo_factura.save()
            else:
                pass

        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorApi(
            accion='Fin de tarea',
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)

def tokenisacion1(request):


    url = 'https://login.microsoftonline.com/common/oauth2/token'

    data = {
        'grant_type': 'password',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'client_id': 'a77e1c67-79c8-4dfb-bc49-27f416a217fb',
        'client_secret': '7ZW8Q~Cbv6hW1vRbK7ZqAd4kutMNQM5kpetIJc8V',
        'username': 'analistati@pcsocial.org',
        'password': 'csAti2017*'
    }

    response = requests.post(url, data=data)

    if response.ok:
        token = response.json()['access_token']
        print('Token de acceso:', token)
    else:
        print('Error al obtener token de acceso:', response.text)


def tokenisacion(request):
    url = "https://192.168.1.2:50000/b1s/v1/Login"

    payload = "{\"CompanyDB\":\"PRUEBAS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

    response = requests.request("POST", url, data=payload, verify=False)
    respuesta = ast.literal_eval(response.text)
    sessionId = respuesta['SessionId']
    url2 = "https://192.168.1.2:50000/b1s/v1/BusinessPartners('P005375')"
    payload_actualizacion = json.dumps({
    "CardName": "ASOCIACION CANASTO DE LA ABUNDANCIA MONIYA KIRIGAI"
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'B1SESSION=' + sessionId
    }

    response = requests.request("PATCH", url2, data=payload_actualizacion, headers=headers, verify=False)

    # Verificar la respuesta de la actualización
    if response.status_code == 204:
        print("Orden de compra actualizada correctamente.")
    else:
        print("Error al actualizar la orden de compra. Código de estado:", response.status_code)




def prueba():
    url = "https://192.168.1.2:50000/b1s/v1/Login"

    payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

    response = requests.request("POST", url, data=payload, verify=False)
    respuesta = ast.literal_eval(response.text)
    empresas= Empresas.objects.all()
    lista_correos = []
    lista_correos_no_existentes = []
    lista_correos_simbolos_especiales = []
    for empresa in empresas:
        try:
            url2 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('TareaEmpresarioSinEmails')/List?NombreEmpresario='" + str(empresa.nombre) + "'"

            headers = {
                'Prefer': 'odata.maxpagesize=999999',
                'Cookie': 'B1SESSION=' + respuesta['SessionId']
            }
            response = requests.request("GET", url2, headers=headers, verify=False)
            response = response.text
            response = response.replace('null', ' " " ')
            response = ast.literal_eval(response)
            response = response['value']
            if response==[]:
                url5 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('validacionempresariossap')/List?NombreEmpresario='" + str(
                    empresa.nombre) + "'"

                headers = {
                    'Prefer': 'odata.maxpagesize=999999',
                    'Cookie': 'B1SESSION=' + respuesta['SessionId']
                }
                response5 = requests.request("GET", url5, headers=headers, verify=False)
                response5 = response5.text
                response5 = response5.replace('null', ' " " ')
                response5 = ast.literal_eval(response5)
                response5 = response5['value']
                if response5 == []:
                    lista_correos_no_existentes.append(str(empresa.nombre))
                else:
                    lista_correos.append(str(empresa.nombre))
            else:
                response=response[0]['E_MailL']
                if response=='':
                    lista_correos.append(str(empresa.nombre))
                else:
                    pass
        except UnicodeEncodeError:
            lista_correos_simbolos_especiales.append(empresa.nombre)

    lista_correos=lista_correos[2:]
    lista_correos_no_existentes=lista_correos_no_existentes[2:]
    if lista_correos==[]:
        pass
    else:
        empresas_str = '\n '.join(lista_correos)
        email = EmailMessage(' EMPRESAS SIN CORREO' ,
                             'las empresas que no tienen correos asignados al titulo LOGISTICA Y DESPACHOS son los siguientes: \n'
                             + empresas_str ,
                             to=['coordtecnologia@pcsocial.org'])
        email.send()
        email = EmailMessage(' EMPRESAS SIN CORREO',
                             'las empresas que no tienen correos asignados al titulo LOGISTICA Y DESPACHOS son los siguientes: \n'
                             + empresas_str,
                             to=['analistati@pcsocial.org'])
        email.send()

    if lista_correos_no_existentes==[]:
        pass
    else:
        empresas_str = '\n '.join(lista_correos_no_existentes)
        email = EmailMessage(' EMPRESAS NO REGISTRADAS' ,
                             'las empresas que no se encuentran registradas en SAP son los siguientes: \n'
                             + empresas_str ,
                             to=['coordtecnologia@pcsocial.org'])
        email.send()
        email = EmailMessage(' EMPRESAS NO REGISTRADAS',
                             'las empresas que no se encuentran registradas en SAP son los siguientes: \n'
                             + empresas_str,
                             to=['analistati@pcsocial.org'])
        email.send()
    if lista_correos_simbolos_especiales==[]:
        pass
    else:
        empresas_str = '\n '.join(lista_correos_simbolos_especiales)
        email = EmailMessage(' EMPRESAS CON SIMBOLOS ESPECIALES' ,
                             'Las empresas que hacen uso de simbolos especiales son las siguientes: \n'
                             + empresas_str ,
                             to=['coordtecnologia@pcsocial.org'])
        email.send()
        email = EmailMessage(' EMPRESAS CON SIMBOLOS ESPECIALES',
                             'Las empresas que hacen uso de simbolos especiales son las siguientes: \n'
                             + empresas_str,
                             to=['analistati@pcsocial.org'])
        email.send()

    url = "https://192.168.1.2:50000/b1s/v1/Logout"
    responselogout = requests.request("POST", url, verify=False)



def pruebacorreo(request):
    email = EmailMessage('SERVICIO FINANCIERO CREDIYA DENEGADO',
                         'Lamentablemente, su Servicio Financiero para el pedido : \n',
                         to=['juansebastianduartes@gmail.com'])
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
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/PurchaseOrders?$orderby=DocDate desc&$select=DocNum,DocEntry,CardCode,CardName&$filter=DocDate eq '" \
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
                if PedidosAlmacenados.objects.filter(pedido=datos['DocNum']).exists():
                    pass
                else:
                    try:
                        dependencias = 'LOGISTICA Y DESPACHOS'
                        url3 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaEmailEmpresa')/List?empresa='" + \
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
                                        email = EmailMessage(str(datos['CardName'])+' TIENES UN NUEVO PEDIDO '+str(datos['DocNum']),
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
                                        pedido_al = PedidosAlmacenados(
                                            pedido=datos['DocNum']
                                        )
                                        pedido_al.save()
                                    except:
                                        now = datetime.now(pytz.timezone('America/Bogota'))
                                        hoy = now.date()
                                        hora = now.time()
                                        errores = HistorialErrorTarea(
                                            accion='Fallo al enviar al correo ' + str(correos),
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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
    except:
        error = str(sys.exc_info()[1])
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Error de conexion: ' + error,
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)






def tarea_correo_pedido_dos():
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
        url = "https://192.168.1.2:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.2:50000/b1s/v1/PurchaseOrders?$orderby=DocDate desc&$select=DocNum,DocEntry,CardCode,CardName&$filter=DocDate eq '" \
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
                if PedidosAlmacenados.objects.filter(pedido=datos['DocNum']).exists():
                    pass
                else:
                    try:
                        dependencias = 'LOGISTICA Y DESPACHOS'
                        url3 = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaEmailEmpresa')/List?empresa='" + \
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
                                        email = EmailMessage(str(datos['CardName'])+' TIENES UN NUEVO PEDIDO '+str(datos['DocNum']),
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
                                        pedido_al = PedidosAlmacenados(
                                            pedido=datos['DocNum']
                                        )
                                        pedido_al.save()
                                    except:
                                        now = datetime.now(pytz.timezone('America/Bogota'))
                                        hoy = now.date()
                                        hora = now.time()
                                        errores = HistorialErrorTarea(
                                            accion='Fallo al enviar al correo ' + str(correos),
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
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)
    except:
        error = str(sys.exc_info()[1])
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()
        errores = HistorialErrorTarea(
            accion='Error de conexion: ' + error,
            fecha=hoy,
            hora=hora,
            empresa='No Corresponde',
            pedido='No Corresponde',
        )
        errores.save()
        url = "https://192.168.1.2:50000/b1s/v1/Logout"
        responselogout = requests.request("POST", url, verify=False)