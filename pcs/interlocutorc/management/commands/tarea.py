from django.core.management.base import BaseCommand
from datetime import datetime
import pytz, requests, ast, sys
from interlocutorc.models import HistorialErrorTarea

class Command(BaseCommand):
    help = 'Envia correo de pedido'

    def handle(self, *args, **kwargs):
        try:
            now = datetime.now(pytz.timezone('America/Bogota'))
            hoy = now.date()
            hora = now.time()

            HistorialErrorTarea.objects.create(
                accion='Inicio de tarea',
                fecha=hoy,
                hora=hora,
                empresa='No Corresponde',
                pedido='No Corresponde',
            )

            url = "https://192.168.1.2:50000/b1s/v1/Login"
            payload = "{\"CompanyDB\":\"PCS\",\"UserName\":\"manager1\",\"Password\":\"HYC909\"}"
            response = requests.request("POST", url, data=payload, verify=False)
            respuesta = ast.literal_eval(response.text)

            HistorialErrorTarea.objects.create(
                accion='Mensaje: ' + str(respuesta),
                fecha=hoy,
                hora=hora,
                empresa='No Corresponde',
                pedido='No Corresponde',
            )

            requests.request("POST", "https://192.168.1.2:50000/b1s/v1/Logout", verify=False)

        except:
            error = str(sys.exc_info()[1])
            HistorialErrorTarea.objects.create(
                accion='Error: ' + error,
                fecha=hoy,
                hora=hora,
                empresa='No Corresponde',
                pedido='No Corresponde',
            )