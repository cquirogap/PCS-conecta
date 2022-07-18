# Import the datetime module so that we can get the current time
import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from interlocutorc.forms import *
from interlocutorc.models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date
from datetime import datetime
import requests
import ast


# Create your views here.
# This view method handles the request for the root URL /
# See urls.py for the mapping.

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

def tarea(request):
    email = EmailMessage('TIENES UN NUEVO PEDIDO',
                         'Ha recibido un pedido nuevo.Para conocer el detalle del pedido ingresa al siguiente link'
                         + '45.56.118.44/configuracion/solicitud_pedido_orden/detalle/',
                         to=['juansebastianduartes@gmail.com'])
    email.send()


def tarea_correo_pedido():
    try:
        estado = 'bost_Open'
        hoy=date.today()
        url = "https://192.168.1.20:50000/b1s/v1/Login"

        payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager\",\"Password\":\"HYC909\"}"

        response = requests.request("POST", url, data=payload, verify=False)

        respuesta = ast.literal_eval(response.text)
        url2 = "https://192.168.1.20:50000/b1s/v1/PurchaseOrders?$orderby=DocDate desc&$select=DocNum,DocEntry,CardCode&$filter=DocDate eq '" \
               + str(hoy) + "'and CardCode eq 'P005050'"

        headers = {
            'Prefer': 'odata.maxpagesize=999999',
            'Cookie': 'B1SESSION=' + respuesta['SessionId']
        }
        response = requests.request("GET", url2, headers=headers, verify=False)
        response = ast.literal_eval(response.text)
        response = response['value']
        for datos in response:
            try:
                pedido_almacenado=PedidosAlmacenados.objects.get(pedido=datos['DocNum'])
                pass
            except:
                try:
                    dependencias='LOGISTICA Y DESPACHOS'
                    url3 = "https://192.168.1.20:50000/b1s/v1/SQLQueries('ConsultaEmailEmpresa')/List?empresa='" + datos['CardCode'] + "'&dependencia='" + dependencias + "'"
                    response2 = requests.request("GET", url3, headers=headers, verify=False)
                    response2 = ast.literal_eval(response2.text)
                    response2 = response2['value']
                    response2 = response2[0]
                    response2 = response2['E_MailL']
                    response2=str(response2).split(";")
                    for correos in response2:
                        email = EmailMessage('TIENES UN NUEVO PEDIDO',
                                                'Ha recibido un pedido nuevo.Para conocer el detalle del pedido ingresa al siguiente link '
                                                + 'http://45.56.118.44/configuracion/solicitud_pedido_orden/detalle/' + str(datos['DocEntry']) + '/',
                                                to=['juansebastianduartes@gmail.com'])
                        email.send()
                    pedido_al = PedidosAlmacenados(
                        pedido=datos['DocNum']
                    )
                    pedido_al.save()
                except:
                    hoy = datetime.now()
                    pedido_al = PedidosAlmacenados(
                        pedido=datos['DocNum']
                    )
                    pedido_al.save()
                    errores = HistorialErrorTarea(
                        accion='No se encuentra correo para el pedido '+str(datos['DocNum']),
                        fecha=hoy,
                    )
                    errores.save()
    except:
        hoy=datetime.now()
        errores = HistorialErrorTarea(
            accion='Error de conexion',
            fecha=hoy,
        )
        errores.save()