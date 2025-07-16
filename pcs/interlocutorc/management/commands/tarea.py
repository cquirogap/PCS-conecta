# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime
import pytz
import requests
import ast
import sys
import re
from django.core.mail import EmailMessage
from interlocutorc.models import HistorialErrorTarea, Empresas, PedidosAlmacenados, HistorialEmailEnviados

class Command(BaseCommand):
    help = 'Envia correos de pedidos nuevos desde SAP'

    def handle(self, *args, **kwargs):
        now = datetime.now(pytz.timezone('America/Bogota'))
        hoy = now.date()
        hora = now.time()

        def registrar_error(mensaje, empresa='No Corresponde', pedido='No Corresponde'):
            HistorialErrorTarea.objects.create(
                accion=mensaje,
                fecha=hoy,
                hora=hora,
                empresa=empresa,
                pedido=pedido,
            )

        try:
            registrar_error('Inicio de tarea')

            # Login SAP
            url_login = "https://192.168.1.2:50000/b1s/v1/Login"
            payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"
            response = requests.post(url_login, data=payload, verify=False)
            respuesta = ast.literal_eval(response.text)
            session_id = respuesta.get('SessionId', None)

            if not session_id:
                registrar_error('Error al obtener SessionId: ' + str(respuesta))
                return

            # Obtener pedidos
            url_pedidos = "https://192.168.1.2:50000/b1s/v1/PurchaseOrders?$orderby=DocDate desc&$select=DocNum,DocEntry,CardCode,CardName&$filter=DocDate eq '" + str(hoy) + "'"
            headers = {
                'Prefer': 'odata.maxpagesize=999999',
                'Cookie': 'B1SESSION=' + session_id
            }
            response = requests.get(url_pedidos, headers=headers, verify=False)
            response = ast.literal_eval(response.text)
            pedidos = response.get('value', [])

            for datos in pedidos:
                nombre_empresa = str(datos['CardName'])
                num_pedido = str(datos['DocNum'])

                if Empresas.objects.filter(nombre=nombre_empresa).exists():
                    if PedidosAlmacenados.objects.filter(pedido=num_pedido).exists():
                        continue

                    try:
                        dependencia = 'LOGISTICA Y DESPACHOS'
                        url_email = "https://192.168.1.2:50000/b1s/v1/SQLQueries('ConsultaEmailEmpresa')/List?empresa='" + datos['CardCode'] + "'&dependencia='" + dependencia + "'"
                        response2 = requests.get(url_email, headers=headers, verify=False)
                        response2 = ast.literal_eval(response2.text).get('value', [])

                        if not response2:
                            registrar_error('No se tiene correo asignado al titulo LOGISTICA Y DESPACHOS', nombre_empresa, num_pedido)
                            continue

                        correos = response2[0]['E_MailL'].split(";")
                        for correo in [c.strip() for c in correos]:
                            if re.match(r"[^@]+@[^@]+\.[^@]+", correo):
                                try:
                                    asunto = nombre_empresa + ' TIENES UN NUEVO PEDIDO ' + num_pedido
                                    mensaje = 'Ha recibido un pedido nuevo.\n\nDetalle del pedido:\nhttp://45.56.118.44/configuracion/solicitud_pedido_orden/detalle/' + str(datos['DocEntry']) + '/'
                                    email = EmailMessage(asunto, mensaje, to=[correo])
                                    email.send()

                                    HistorialEmailEnviados.objects.create(
                                        fecha=hoy,
                                        hora=hora,
                                        empresa=nombre_empresa,
                                        pedido=num_pedido,
                                        tipo='enviado',
                                        email=correo
                                    )

                                    PedidosAlmacenados.objects.create(pedido=num_pedido)

                                except Exception as e:
                                    registrar_error('Fallo al enviar al correo ' + correo, nombre_empresa, num_pedido)
                            else:
                                registrar_error('Correo no válido: ' + correo, nombre_empresa, num_pedido)

                    except Exception as e:
                        registrar_error('No se envió el correo', nombre_empresa, num_pedido)

                else:
                    HistorialEmailEnviados.objects.create(
                        fecha=hoy,
                        hora=hora,
                        empresa=nombre_empresa,
                        pedido=num_pedido,
                        tipo='noregistrado',
                        email=None
                    )

            registrar_error('Fin de tarea')

        except Exception:
            registrar_error('Error de conexión: ' + str(sys.exc_info()[1]))

        finally:
            try:
                requests.post("https://192.168.1.2:50000/b1s/v1/Logout", verify=False)
            except:
                pass