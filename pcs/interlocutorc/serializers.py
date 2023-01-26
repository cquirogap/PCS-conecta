from rest_framework.serializers import ModelSerializer
from interlocutorc.models import ClientesApi

class PostSerializer(ModelSerializer):
    class Meta:
        model= ClientesApi
        fields=['NombreEmpresa','Identificacion','TipoIdentificacion','Correo','ValorOrden','FechaEntrega','FechaPago','NumeroPedido']