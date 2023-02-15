from rest_framework.routers import DefaultRouter
from interlocutorc.views import ApiPrueba,ApiFacturas,RespuestaOrdenApi,RespuestaFacturaApi

router_posts=DefaultRouter()

router_posts.register(prefix='post',basename='post',viewset=ApiPrueba)
router_posts.register(prefix='facturas',basename='facturas',viewset=ApiFacturas)
router_posts.register(prefix='respuesta_orden_compra',basename='respuesta_orden_compra',viewset=RespuestaOrdenApi)
router_posts.register(prefix='respuesta_factura',basename='respuesta_factura',viewset=RespuestaFacturaApi)