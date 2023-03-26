from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from interlocutorc.models import ClientesApi,FacturasApi,RespuestaOrdenCompraApi,RespuestaFacturaApi




class MyDataSerializer(serializers.Serializer):
    OrdenEDI = serializers.CharField()
    OrdenSAP = serializers.CharField()
    Cliente = serializers.CharField()
    Empresario = serializers.CharField()
    NombreCliente = serializers.CharField()
    NombreEmpresario = serializers.CharField()
    GLNEntrega = serializers.CharField()
    SitioEntrega = serializers.CharField()
    FechaExpedicionEDI = serializers.CharField()
    FechaMinimaEdi = serializers.CharField()
    FechaMaximaEdi = serializers.CharField()
    GLNCod_Dep = serializers.CharField()
    NombreDep = serializers.CharField()	
    GLNCliente = serializers.CharField()
    Tipopedido = serializers.CharField()
    lineas_orden = serializers.JSONField()



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
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroOrdenCompra','FechaEmision','Interes']


class RespuestaFacturaSerializer(ModelSerializer):
    class Meta:
        model= RespuestaFacturaApi
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroFactura','FechaEmision','Interes']