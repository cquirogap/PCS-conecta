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
        current_user = request.user
        permisos = Permisos.objects.filter(usuario_id=current_user.id).first()
        usuario_datos = Usuarios_datos.objects.filter(usuario_id=current_user.id).first()
        historial = HistoriaUsuario(
            usuario_id=int(current_user.id),
            empresa_id=int(usuario_datos.empresa_id),
            accion='Logueo de Usuario',
            fecha=timezone.now(),
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


