from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from interlocutorc.models import ClientesApi,FacturasApi,RespuestaOrdenCompraApi,RespuestaFacturaApi,RespuestaOrdenCompraApis
import copy



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
        fields=['NombreEmpresa','Identificacion','TipoIdentificacion','Correo','ValorFacturaEmitida','FechaPagoFactura','NumeroFactura','Referencia2']



class RespuestaOrdenSerializer(ModelSerializer):
    class Meta:
        model= RespuestaOrdenCompraApi
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroOrdenCompra','FechaEmision','Interes']


class RespuestaFacturaSerializer(ModelSerializer):
    class Meta:
        model= RespuestaFacturaApi
        fields=['Identificacion','TipoIdentificacion','ValorAprobado','NumeroFactura','FechaEmision','Interes']


class RespuestaOrdenesSerializer(serializers.Serializer):
    NombreEmpresa = serializers.CharField()
    Identificacion = serializers.CharField()
    TipoIdentificacion = serializers.CharField()
    ReferenciaOrdenes = serializers.CharField()
    Ordenes = serializers.ListField()

    def create(self, validated_data):
        nombre_empresa = validated_data.get('NombreEmpresa', '')
        identificacion = validated_data.get('Identificacion', '')
        tipo_identificacion = validated_data.get('TipoIdentificacion', '')
        referencia_ordenes = validated_data.get('ReferenciaOrdenes', '')
        ordenes_data = validated_data.get('Ordenes', [])

        created_instances = []  # To collect the created instances

        for orden_data in ordenes_data:
            created_instance = RespuestaOrdenCompraApis.objects.create(
                NombreEmpresa=nombre_empresa,
                Identificacion=identificacion,
                TipoIdentificacion=tipo_identificacion,
                ReferenciaOrdenes=referencia_ordenes,
                ValorAprobado=orden_data.get('ValorAprobado', ''),
                FechaEmision=orden_data.get('FechaEmision', ''),
                Interes=orden_data.get('Interes', ''),
                NumeroOrdenCompra=orden_data.get('NumeroOrdenCompra', ''),
                Estado=orden_data.get('Estado', '')
            )
            created_instances.append(created_instance)

        return created_instances



class OrdenSerializer(serializers.Serializer):
    ValorAprobado = serializers.CharField()
    FechaEmision = serializers.DateField()
    Interes = serializers.CharField()
    NumeroOrdenCompra = serializers.CharField()
    Estado = serializers.IntegerField()

class RespuestaOrdeneSerializer(serializers.ModelSerializer):
    Ordenes = OrdenSerializer(many=True)

    class Meta:
        model = RespuestaOrdenCompraApis
        fields = ['NombreEmpresa', 'Identificacion', 'TipoIdentificacion', 'ReferenciaOrdenes', 'Ordenes']

    def create(self, validated_data):
        ordenes_data = validated_data.pop('Ordenes')
        respuesta_orden = RespuestaOrdenCompraApi.objects.create(**validated_data)

        for orden_data in ordenes_data:
            OrdenCompraApi.objects.create(RespuestaOrden=respuesta_orden, **orden_data)

        return respuesta_orden