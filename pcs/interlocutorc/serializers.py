from rest_framework.serializers import ModelSerializer
from interlocutorc.models import ClientesApi,FacturasApi,RespuestaOrdenCompraApi,RespuestaFacturaApi

class PostSerializer(ModelSerializer):
    class Meta:
        model= ClientesApi
        fields=['NombreEmpresa','Identificacion','TipoIdentificacion','Correo','ValorOrden','FechaEntrega','FechaPago','NumeroPedido']


class FacturasSerializer(ModelSerializer):
    class Meta:
        model= FacturasApi
        fields=['NombreEmpresa','Identificacion','TipoIdentificacion','Correo','ValorFacturaEmitida','FechaPagoFactura','NumeroFactura']



class RespuestaOrdenSerializer(ModelSerializer):
    class Meta:
        model= RespuestaOrdenCompraApi
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroOrdenCompra','FechaEmision']


class RespuestaFacturaSerializer(ModelSerializer):
    class Meta:
        model= RespuestaFacturaApi
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroFactura','FechaEmision']