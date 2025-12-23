"""Fundacionrv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from interlocutorc.router import router_posts
from pcs import settings
from interlocutorc import views as interlocutorc_views
from configuracion import views as configuracion_views

from rest_framework.authtoken import views as views_api


urlpatterns = [
    url(r'^admin123/', admin.site.urls),
    url(r'^api/', include(router_posts.urls)),
    url(r'^login_api/',views_api.obtain_auth_token),

]
urlpatterns.extend(
    [


        # Administracion
        url(r'^administracion/$', interlocutorc_views.panel_administracion, name="admin-panel"),
        url(r'^ayuda/$', interlocutorc_views.panel_ayuda, name="admin-panel"),
        url(r'^prueba/$', interlocutorc_views.tarea_correo_pedido),
        url(r'^prueba_factura/$', interlocutorc_views.pruebacorreosfactura),
        url(r'^pruebasap/$', interlocutorc_views.prubasap2),
        url(r'^pruebanueva/$', configuracion_views.tarea_correo_pedido_tres),
        url(r'^pruebacorreo/$', interlocutorc_views.pruebacorreo),
        url(r'^prueba_servicio/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$', interlocutorc_views.MyListView.as_view()),
        url(r'^api/pedidos/(?P<fecha>\d{4}-\d{2}-\d{2})/$', interlocutorc_views.ApiPedidos.as_view(), name="api_pedidos"),
        #_______________________________________________ CONFIGURACION _____________________________________________
        #Justificacion
        url(r'^configuracion/justificacion/$', configuracion_views.config_justificacion),
        url(r'^configuracion/justificacion/registrar/$', configuracion_views.config_justificacion_registrar),
        url(r'^configuracion/justificacion/editar/(?P<id>[-\w]+)/$', configuracion_views.config_justificacion_editar),
        url(r'^configuracion/justificacion/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_justificacion_borrar),
        #Perfiles PCS
        url(r'^configuracion/perfiles_pcs/$', configuracion_views.config_perfiles_pcs),
        url(r'^configuracion/perfiles_pcs/registrar/$', configuracion_views.config_perfiles_registrar),
        url(r'^configuracion/perfiles_pcs/editar/(?P<id>[-\w]+)/$', configuracion_views.config_perfiles_editar),
        url(r'^configuracion/perfiles_pcs/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_perfiles_borrar),
        # Continentes
        url(r'^configuracion/continentes/$', configuracion_views.config_continentes),
        url(r'^configuracion/continentes/registrar/$', configuracion_views.config_continentes_registrar),
        url(r'^configuracion/continentes/editar/(?P<id>[-\w]+)/$', configuracion_views.config_continentes_editar),
        url(r'^configuracion/continentes/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_continentes_borrar),
        # Paises
        url(r'^configuracion/paises/$', configuracion_views.config_paises),
        url(r'^configuracion/paises/registrar/$', configuracion_views.config_paises_registrar),
        url(r'^configuracion/paises/editar/(?P<id>[-\w]+)/$', configuracion_views.config_paises_editar),
        url(r'^configuracion/paises/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_paises_borrar),
        url(r'^configuracion/paises/datos/$', configuracion_views.config_paises_datos),
        # Departamentos
        url(r'^configuracion/departamentos/$', configuracion_views.config_departamentos),
        url(r'^configuracion/departamentos/registrar/$', configuracion_views.config_departamentos_registrar),
        url(r'^configuracion/departamentos/editar/(?P<id>[-\w]+)/$', configuracion_views.config_departamentos_editar),
        url(r'^configuracion/departamentos/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_departamentos_borrar),
        url(r'^configuracion/departamentos/datos/$', configuracion_views.config_departamentos_datos),
        # Municicpios
        url(r'^configuracion/municipios/$', configuracion_views.config_municipios),
        url(r'^configuracion/municipios/registrar/$', configuracion_views.config_municipios_registrar),
        url(r'^configuracion/municipios/editar/(?P<id>[-\w]+)/$', configuracion_views.config_municipios_editar),
        url(r'^configuracion/municipios/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_municipios_borrar),
        url(r'^configuracion/municipios/datos/$', configuracion_views.config_municipios_datos),
        #Atencion
        url(r'^configuracion/areas_atencion/$', configuracion_views.config_areas_atencion),
        url(r'^configuracion/areas_atencion/registrar/$', configuracion_views.config_areas_atencion_registrar),
        url(r'^configuracion/areas_atencion/editar/(?P<id>[-\w]+)/$', configuracion_views.config_areas_atencion_editar),
        url(r'^configuracion/areas_atencion/editar_integrantes/(?P<id>[-\w]+)/$', configuracion_views.config_areas_atencion_editar_integrantes),
        url(r'^configuracion/areas_atencion/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_areas_atencion_borrar),

        #Peticiones
        url(r'^configuracion/peticion/$', configuracion_views.config_peticiones),
        url(r'^configuracion/peticion/registrar/$', configuracion_views.config_peticiones_registrar),
        url(r'^configuracion/peticion/editar/(?P<id>[-\w]+)/$', configuracion_views.config_peticiones_editar),
        url(r'^configuracion/peticion/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_peticiones_borrar),

        #Personas
        url(r'^configuracion/personas_aten/$', configuracion_views.config_personas_atencion),
        url(r'^configuracion/personas_aten/registrar/$', configuracion_views.config_personas_aten_registrar),
        url(r'^configuracion/personas_aten/editar/(?P<id>[-\w]+)/$', configuracion_views.config_personas_aten_editar),
        url(r'^configuracion/personas_aten/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_personas_aten_borrar),

        #Solicitudes
        url(r'^configuracion/solicitudes/$', configuracion_views.config_solicitudes),
        url(r'^configuracion/respuesta_factura/$', configuracion_views.config_respuesta_factura_pedido),
        url(r'^configuracion/solicitudes_generales/$', configuracion_views.config_solicitudes_generales),
        url(r'^configuracion/solicitudes_generales/informacion/$', configuracion_views.informacion_complementaria_consulta_solicitud),
        url(r'^configuracion/pedidos_otros_canales/informacion/$', configuracion_views.informacion_pedidos_otros_canales_solicitud),
        url(r'^configuracion/pedidos_otros_canales/informacion_cliente/$', configuracion_views.informacion_pedidos_otros_canales_solicitud_cliente),
        url(r'^configuracion/pedidos_otros_canales_empresarios/informacion/$', configuracion_views.informacion_pedidos_otros_canales_empresario_solicitud),
        url(r'^configuracion/pedidos_otros_canales_empresarios/facturar/$', configuracion_views.informacion_pedidos_otros_canales_empresario_facturar),
        url(r'^configuracion/pedidos_otros_canales_empresarios/recibo/$', configuracion_views.informacion_pedidos_otros_canales_empresario_recibo),


        #Otros Pedidos
        url(r'^configuracion/orden_cliente_otroscanales/$', configuracion_views.config_ordenes_otroscanales),
        url(r'^ruta/obtener/imagen/$', configuracion_views.obtener_imagen_producto),
        url(r'^configuracion/orden_pcs_otroscanales/$', configuracion_views.config_ordenes_otroscanales_pcs),
        url(r'^configuracion/orden_pcs_otroscanales_cliente/$', configuracion_views.config_ordenes_otroscanales_pcs_cliente),
        url(r'^configuracion/orden_empresiario_otroscanales/$', configuracion_views.config_ordenes_otroscanales_empresario),
        url(r'^configuracion/solicitud_asignacion/descargar_zip/$', configuracion_views.descargar_pedidos_zip),
        url(r'^configuracion/orden_empresiario_otroscanales_facturar/$', configuracion_views.config_ordenes_otroscanales_empresario_facturacion),
        url(r'^configuracion/orden_empresiario_otroscanales_recibo/$', configuracion_views.config_ordenes_otroscanales_empresario_recibo),
        url(r'^configuracion/imagen_empresiario_otroscanales/$', configuracion_views.config_imagen_otroscanales_empresario),
        url(r'^configuracion/imagen_empresiario_otroscanales/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_imagen_otroscanales_empresario_borrar),
        url(r'^configuracion/registrar/imagen_empresiario_otroscanales/$', configuracion_views.config_imagen_otroscanales_empresario_registrar),
        url(r'^configuracion/registrar/imagen_empresiario_otroscanales_masivo/$', configuracion_views.config_imagen_otroscanales_empresario_registrar_masivo),
        url(r'^configuracion/orden_pcs_otroscanales/detalle/(?P<id>[-\w]+)/$', configuracion_views.config_ordenes_otroscanales_pcs_detalle),
        url(r'^configuracion/orden_pcs_otroscanales/eliminar/(?P<id>[-\w]+)/$', configuracion_views.config_ordenes_otroscanales_pcs_eliminar),
        url(r'^configuracion/orden_pcs_otroscanales/producto/eliminar/(?P<id>[-\w]+)/$', configuracion_views.config_ordenes_otroscanales_pcs_producto_eliminar),
        url(r'^configuracion/orden_pcs_otroscanales/detalle_edi/$', configuracion_views.config_ordenes_otroscanales_pcs_detalle_edi),
        url(r'^configuracion/orden_compra/edi_depacho/$', configuracion_views.config_ordenes_aviso_despacho_detalle_edi),
        url(r'^configuracion/orden_pcs_otroscanales_cliente/detalle/(?P<id>[-\w]+)/$', configuracion_views.config_ordenes_otroscanales_pcs_detalle_cliente),
        url(r'^configuracion/orden_pcs_otroscanales_cliente/eliminar/(?P<id>[-\w]+)/$', configuracion_views.config_ordenes_otroscanales_pcs_eliminar_cliente),
        url(r'^configuracion/orden_pcs_otroscanales/detalles/$', configuracion_views.config_ordenes_otroscanales_pcs_detalles),
        url(r'^configuracion/orden_pcs_otroscanales_plus/detalles/$', configuracion_views.config_ordenes_otroscanales_pcs_plus_detalles),
        url(r'^configuracion/orden_pcs_otroscanales/detalles_todos/$', configuracion_views.config_ordenes_otroscanales_pcs_detalles_todos),
        url(r'^configuracion/orden_pcs_otroscanales/estado/$', configuracion_views.config_ordenes_otroscanales_pcs_estado),
        url(r'^configuracion/orden_pcs_otroscanales/fecha_minima/$', configuracion_views.config_ordenes_otroscanales_pcs_fecha_minima),
        url(r'^configuracion/orden_pcs_otroscanales/fecha_maxima/$', configuracion_views.config_ordenes_otroscanales_pcs_fecha_maxima),


        #Registrar crediya y Credilisto
        url(r'^configuracion/documentos_creditos/$', configuracion_views.config_documentos_creditos),
        url(r'^configuracion/registrar_documentos_creditos/$', configuracion_views.config_registro_documentos_creditos),
        url(r'^configuracion/editar_documentos_creditos/(?P<id>[-\w]+)/$', configuracion_views.config_editar_documentos_creditos),
        url(r'^configuracion/historial_documentos_creditos/(?P<id>[-\w]+)/$', configuracion_views.config_historial_documentos_creditos),
        url(r'^configuracion/servicio_crediya_registro/$', configuracion_views.config_servicio_crediya_registro),
        url(r'^configuracion/servicio_crediya_preaprobado/$', configuracion_views.config_servicio_crediya_preaprobado),
        url(r'^configuracion/servicio_crediya_preaprobados/$', configuracion_views.config_servicio_crediya_preaprobados),
        url(r'^configuracion/servicio_crediya_lista/$', configuracion_views.config_servicio_crediya_lista),
        url(r'^configuracion/servicio_credilisto_lista/$', configuracion_views.config_servicio_credilisto_lista),
        url(r'^configuracion/servicio_codigo_registro_lista/$', configuracion_views.config_servicio_codigoregistro_lista),
        url(r'^configuracion/servicio_crediya_consulta/$', configuracion_views.config_crediya_consulta_generales),
        url(r'^configuracion/servicio_credilisto_consulta/$', configuracion_views.config_credilisto_consulta_generales),
        url(r'^configuracion/servicio_crediya_historial/$', configuracion_views.config_crediya_consulta_historial),
        url(r'^configuracion/servicio_credilisto_historial/$', configuracion_views.config_credilisto_consulta_historial),
        url(r'^configuracion/servicio_crediya_historial/informacion/$', configuracion_views.informacion_complementaria_historial_crediya),
        url(r'^configuracion/servicio_credilisto_historial/informacion/$', configuracion_views.informacion_complementaria_historial_credilisto),
        url(r'^configuracion/servicio_crediya_consulta/informacion/$', configuracion_views.informacion_complementaria_consulta_crediya),
        url(r'^configuracion/servicio_credilisto_consulta/informacion/$', configuracion_views.informacion_complementaria_consulta_credilisto),
        url(r'^configuracion/servicio_credilisto_consulta/cruces/$', configuracion_views.informacion_complementaria_consulta_cruces_credilisto),
        url(r'^configuracion/servicio_credilisto_registro/$', configuracion_views.config_servicio_credilisto_registro),
        url(r'^configuracion/servicio_codigosregistro_registro/$', configuracion_views.config_servicio_codigoregistro_registro),
        url(r'^configuracion/servicio_empresa_registro_automatico/$', configuracion_views.config_servicio_registro_empresas_aut),
        #PowerBi
        url(r'^configuracion/definiciones/graficas/$', configuracion_views.admin_graficas_powerbi),
        url(r'^configuracion/facturacion/otros_canales/$', configuracion_views.facturacion_otros_canales),
        url(r'^configuracion/recibo/otros_canales/$', configuracion_views.recibo_otros_canales),
        url(r'^configuracion/definiciones/grafica/(?P<grafica_id>\d+)/detalle/$', configuracion_views.detalle_grafica),
        url(r'^configuracion/definiciones/borrar_grafica/(?P<grafica_id>[-\w]+)/$', configuracion_views.config_graficas_borrar),
        url(r'^configuracion/definiciones/grafica_pcs_actuales/$', configuracion_views.admin_graficas_actuales_pcs_powerbi),
        url(r'^configuracion/definiciones/grafica_empresario_clientes/$', configuracion_views.admin_graficas_empresario_cliente_powerbi),
        url(r'^configuracion/definiciones/grafica_empresarios_actuales/$', configuracion_views.admin_graficas_actuales_empresarios_powerbi),
        url(r'^configuracion/definiciones/grafica_comercial/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_comerciales_powerbi),
        url(r'^configuracion/definiciones/grafica_exportaciones/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_exportaciones_powerbi),
        url(r'^configuracion/definiciones/grafica_desarrollo_empresarial/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_desarrollo_empresarial_powerbi),
        url(r'^configuracion/definiciones/grafica_administrativo_financiero/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_administrativo_financiero_powerbi),
        url(r'^configuracion/definiciones/grafica_mercadeo_innovacion/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_mercadeo_innovacion_powerbi),
        url(r'^configuracion/definiciones/grafica_operaciones_logistica/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_operaciones_logistica_powerbi),
        url(r'^configuracion/definiciones/grafica_adicional/(?P<grafica_id>\w+)/$', configuracion_views.admin_graficas_adicional_powerbi),
        url(r'^configuracion/definiciones/grafica_formacion/$', configuracion_views.admin_graficas_formacion_powerbi),
        url(r'^configuracion/definiciones/grafica_formacion_empresario/$', configuracion_views.admin_graficas_formacion_empresario_powerbi),
        url(r'^configuracion/definiciones/grafica_formacion_cliente/$', configuracion_views.admin_graficas_formacion_cliente_powerbi),

        #RespuestaPedido
        url(r'^configuracion/respuesta_pedido/$', configuracion_views.config_respuesta_pedido),
        url(r'^configuracion/respuesta_seg_pedido/$', configuracion_views.config_respuesta_seg_pedido),
        url(r'^configuracion/respuesta_ter_pedido/$', configuracion_views.config_respuesta_ter_pedido),
        url(r'^configuracion/respuesta_cuar_pedido/$', configuracion_views.config_respuesta_cuar_pedido),
        url(r'^configuracion/respuesta_quin_pedido/$', configuracion_views.config_respuesta_quin_pedido),
        url(r'^configuracion/respuesta_sex_pedido/$', configuracion_views.config_respuesta_sex_pedido),
        url(r'^configuracion/respuesta_sept_pedido/$', configuracion_views.config_respuesta_sept_pedido),
        url(r'^configuracion/respuesta_oct_pedido/$', configuracion_views.config_respuesta_oct_pedido),
        url(r'^configuracion/respuesta_peticion/$', configuracion_views.config_respuesta_peticion),
        # Tipos de Radicados
        url(r'^configuracion/tipos_radicados/$', configuracion_views.config_tipos_radicados),
        url(r'^configuracion/tipos_radicados/registrar/$', configuracion_views.config_tipos_radicados_registrar),
        url(r'^configuracion/tipos_radicados/editar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_radicados_editar),
        url(r'^configuracion/tipos_radicados/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_radicados_borrar),
        # Tipos de Envios
        url(r'^configuracion/tipos_envios/$', configuracion_views.config_tipos_envios),
        url(r'^configuracion/tipos_envios/registrar/$', configuracion_views.config_tipos_envios_registrar),
        url(r'^configuracion/tipos_envios/editar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_envios_editar),
        url(r'^configuracion/tipos_envios/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_envios_borrar),
        # Formas de Envios
        url(r'^configuracion/formas_envios/$', configuracion_views.config_formas_envios),
        url(r'^configuracion/formas_envios/registrar/$', configuracion_views.config_formas_envios_registrar),
        url(r'^configuracion/formas_envios/editar/(?P<id>[-\w]+)/$', configuracion_views.config_formas_envios_editar),
        url(r'^configuracion/formas_envios/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_formas_envios_borrar),
        # Perfiles
        url(r'^configuracion/empresas/$', configuracion_views.config_empresas),
        url(r'^configuracion/empresas/registrar/$', configuracion_views.config_empresas_registrar),
        url(r'^configuracion/empresas/editar/(?P<id>[-\w]+)/$', configuracion_views.config_empresas_editar),
        url(r'^configuracion/empresas/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_empresas_borrar),
        url(r'^configuracion/historial_empresas/$', configuracion_views.config_historial_empresas),
        url(r'^configuracion/historial_detalle_pedidos/$', configuracion_views.config_historial_detalle_pedidos),
        url(r'^configuracion/servicio_crediya/$', configuracion_views.config_servicio_crediya),
        url(r'^configuracion/informe_recibo/$', configuracion_views.config_informe_recibo),
        url(r'^configuracion/informe_pedido_otros_can/$', configuracion_views.config_informe_pedido_otros_can),
        url(r'^configuracion/informe_pedido_otros_can_cliente/$', configuracion_views.config_informe_pedido_otros_can_cliente),
        url(r'^configuracion/informe_cliente_fact/$', configuracion_views.config_informe_cliente_fact),
        url(r'^configuracion/servicio_crediya/informe/$', configuracion_views.config_servicio_crediya_informe),
        url(r'^configuracion/servicio_credilisto/informe/$', configuracion_views.config_servicio_credilisto_informe),
        url(r'^configuracion/servicio_credilisto/$', configuracion_views.config_servicio_credilisto),
        url(r'^configuracion/historial_empresas/excel_general/$', configuracion_views.reporte_historial_empresa),
        url(r'^configuracion/generacion_facturas/excel_general/$', configuracion_views.reporte_generacion_facturas),
        url(r'^configuracion/servicio_crediya/excel_general/$', configuracion_views.reporte_servicio_crediya),
        url(r'^configuracion/generarcion_informe/facturas/$', configuracion_views.reporte_facturas_activas),
        url(r'^configuracion/servicio_crediya/informe/excel_general/$', configuracion_views.reporte_servicio_crediya_informe),
        url(r'^configuracion/servicio_credilisto/informe/excel_general/$', configuracion_views.reporte_servicio_credilisto_informe),
        url(r'^configuracion/servicio_credilisto/excel_general/$', configuracion_views.reporte_servicio_credilisto),
        url(r'^configuracion/historial_email/$', configuracion_views.config_historial_email),
        url(r'^configuracion/reenviar_pedido/$', configuracion_views.config_reenviar_pedido),
        url(r'^configuracion/historial_estado_sistema/$', configuracion_views.config_historial_estado_sistema),
        url(r'^configuracion/estado_sistema/$', configuracion_views.config_estado_sistema),
        url(r'^configuracion/historial_respuesta_pedido/$', configuracion_views.config_historial_respuesta_pedido),
        url(r'^configuracion/historial_correos_enviados/$', configuracion_views.config_historial_correos_enviados),
        url(r'^configuracion/historial_codigos_registro/$', configuracion_views.config_historial_codigos_registro),
        url(r'^configuracion/consultar/empresas_codigos/datos/$', configuracion_views.config_consulta_empresario_tipo_codigos),
        url(r'^configuracion/historial_correos_creditos/$', configuracion_views.config_historial_correos_creditos),
        url(r'^configuracion/historial_correos_creditos_errores/$', configuracion_views.config_historial_correos_creditos_error),
        url(r'^configuracion/historial_correos_no_enviados/$', configuracion_views.config_historial_correos_no_enviados),
        url(r'^configuracion/enviar_correos_no_enviados/$', configuracion_views.config_enviar_correos_no_enviados),
        url(r'^configuracion/historial_correos_no_registrados/$', configuracion_views.config_historial_correos_no_registrados),
        url(r'^configuracion/indicadores_envio_email/$', configuracion_views.config_indicadores_envio_emails),
        url(r'^configuracion/envio_mail_indicador/$', configuracion_views.indienvio_mail, name="indienvio_mail"),
        url(r'^configuracion/historial_email/excel_reenviado/$', configuracion_views.reporte_historial_reenviado),
        url(r'^configuracion/historial_email/excel_general/$', configuracion_views.reporte_historial),
        url(r'^configuracion/historial_respuesta_pedido/excel_general/$', configuracion_views.reporte_historial_respuesta),
        url(r'^configuracion/historial_correos_enviados/excel_general/$', configuracion_views.reporte_correos_enviados),
        #Excel Prueba
        url(r'^configuracion/excel_pedidos_externos/$', configuracion_views.config_excel_pedidos_externos),
        url(r'^configuracion/excel_pedidos_externos_distribuido/$', configuracion_views.config_excel_pedidos_externos_distribuido),
        url(r'^configuracion/plantilla_excel_pedidos_externos/$', configuracion_views.config_plantilla_excel_pedidos_externos),
        url(r'^configuracion/plantilla_excel_pedidos_externos_distribuido/$', configuracion_views.config_plantilla_excel_pedidos_externos_distribuido),
        # Soportes
        url(r'^configuracion/soportes/$', configuracion_views.config_soportes),
        url(r'^configuracion/soportes/registrar/$', configuracion_views.config_soportes_registrar),
        url(r'^configuracion/soportes/editar/(?P<id>[-\w]+)/$', configuracion_views.config_soportes_editar),
        url(r'^configuracion/soportes/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_soportes_borrar),
        # Medios Recepcion
        url(r'^configuracion/medios_recepcion/$', configuracion_views.config_medios_recepcion),
        url(r'^configuracion/medios_recepcion/registrar/$', configuracion_views.config_medios_recepcion_registrar),
        url(r'^configuracion/medios_recepcion/editar/(?P<id>[-\w]+)/$', configuracion_views.config_medios_recepcion_editar),
        url(r'^configuracion/medios_recepcion/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_medios_recepcion_borrar),
        # Tipos Devoluciones
        url(r'^configuracion/tipos_devoluciones/$', configuracion_views.config_tipos_devoluciones),
        url(r'^configuracion/tipos_devoluciones/registrar/$', configuracion_views.config_tipos_devoluciones_registrar),
        url(r'^configuracion/tipos_devoluciones/editar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_devoluciones_editar),
        url(r'^configuracion/tipos_devoluciones/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_devoluciones_borrar),
        # Tipos Anulaciones
        url(r'^configuracion/tipos_anulaciones/$', configuracion_views.config_tipos_anulaciones),
        url(r'^configuracion/tipos_anulaciones/registrar/$', configuracion_views.config_tipos_anulaciones_registrar),
        url(r'^configuracion/tipos_anulaciones/editar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_anulaciones_editar),
        url(r'^configuracion/tipos_anulaciones/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_anulaciones_borrar),
        # Tipos de Documentos
        url(r'^configuracion/tipos_documentos/$', configuracion_views.config_tipos_documentos),
        url(r'^configuracion/tipos_documentos/registrar/$', configuracion_views.config_tipos_documentos_registrar),
        url(r'^configuracion/tipos_documentos/editar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_documentos_editar),
        url(r'^configuracion/tipos_documentos/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_tipos_documentos_borrar),
        # Fechas Festivos
        url(r'^configuracion/fechas_festivos/$', configuracion_views.config_fechas_festivos),
        url(r'^configuracion/fechas_festivos/registrar/$', configuracion_views.config_fechas_festivos_registrar),
        url(r'^configuracion/fechas_festivos/editar/(?P<id>[-\w]+)/$', configuracion_views.config_fechas_festivos_editar),
        url(r'^configuracion/fechas_festivos/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_fechas_festivos_borrar),
        # Consecutivos
        url(r'^configuracion/consecutivos/$', configuracion_views.config_consecutivos),
        url(r'^configuracion/consecutivos/historial_carpeta/$', configuracion_views.config_consecutivos_historial_carpeta),
        url(r'^configuracion/consecutivos/historial/$', configuracion_views.config_consecutivos_historial),
        url(r'^configuracion/consecutivos/registrar/$', configuracion_views.config_consecutivos_registrar),
        url(r'^configuracion/consecutivos/editar/(?P<id>[-\w]+)/$', configuracion_views.config_consecutivos_editar),
        url(r'^configuracion/consecutivos/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_consecutivos_borrar),
        url(r'^configuracion/consecutivos/anos/$', configuracion_views.config_consecutivos_anos),
        url(r'^configuracion/consecutivos/anos/actualizar/$', configuracion_views.config_consecutivos_anos_actualizar),
        url(r'^configuracion/consecutivos/actualizar/$', configuracion_views.config_consecutivos_actualizar),


        # Terceros
        url(r'^configuracion/terceros/$', configuracion_views.config_terceros),
        url(r'^configuracion/terceros/registrar/$', configuracion_views.config_terceros_registrar),
        url(r'^configuracion/terceros/editar/(?P<id>[-\w]+)/$', configuracion_views.config_terceros_editar),
        # Tipo Identificacion
        #url(r'^configuracion/tipos_identificacion/$', configuracion_views.config_tipos_identificacion),
        # Usuarios
        url(r'^configuracion/usuario/$', configuracion_views.config_fechas_festivos),
        url(r'^configuracion/usuarios/$', configuracion_views.config_usuarios),
        url(r'^configuracion/usuarios/perfil/$', configuracion_views.config_usuarios_perfil),
        url(r'^configuracion/usuarios/perfil_empresa/$', configuracion_views.config_usuarios_perfil_empresa),
        url(r'^configuracion/asignar_certificados/$', configuracion_views.procesar_pdfs),
        url(r'^configuracion/usuarios/perfil_empresa_despacho/$', configuracion_views.config_usuarios_perfil_empresa_despacho),
        url(r'^configuracion/usuarios/registrar/$', configuracion_views.config_usuarios_registrar),
        url(r'^registrar/usuarios_externos/$', configuracion_views.config_usuarios_registrar_externos),
        url(r'^registrar/usuarios_externos_atencion/$', configuracion_views.config_usuarios_aten_registrar_externos),
        url(r'^registrar/usuarios_externos_creditos/$', configuracion_views.config_usuarios_creditos_registrar_externos),
        url(r'^registrar/usuarios_externos_despacho_diesnueve/$', configuracion_views.config_usuarios_creditos_registrar_despacho_nueve),
        url(r'^registrar/usuarios_externos_despacho_veintedos/$', configuracion_views.config_usuarios_creditos_registrar_despacho_dos),
        url(r'^registrar/usuarios_otros_canales_atencion/$', configuracion_views.config_usuarios_otros_canales_registrar_externos),
        url(r'^registrar/usuarios_externos_pcs/(?P<id>[-\w]+)/$', configuracion_views.config_usuarios_pcs_registrar_externos),
        url(r'^registrar/usuarios_externos_comp/$', configuracion_views.config_usuarios_registrar_externos_comp),
        url(r'^registrar/olvidar_contrasena/$', configuracion_views.config_usuarios_olvidar_contrasena),
        url(r'^configuracion/usuarios/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_usuarios_borrar),
        url(r'^configuracion/usuarios/editar/(?P<id>[-\w]+)/$', configuracion_views.config_usuarios_editar),


        # Dependencias
        url(r'^configuracion/dependencias/$', configuracion_views.config_dependencias),
        url(r'^configuracion/dependencias/registrar/$', configuracion_views.config_dependencias_registrar),
        url(r'^configuracion/dependencias/editar/(?P<id>[-\w]+)/$', configuracion_views.config_dependencias_editar),
        url(r'^configuracion/dependencias/borrar/(?P<id>[-\w]+)/$', configuracion_views.config_dependencias_borrar),

        #_______________________________________________ ADMINISTRACION _____________________________________________




        # Sub Series
        url(r'^configuracion/subseries/$', configuracion_views.config_subseries),
        url(r'^configuracion/subseries/registrar/$', configuracion_views.config_subseries_registrar),
        url(r'^configuracion/subseries/editar/(?P<id>[-\w]+)/$', configuracion_views.config_subseries_editar),
        # TRD
        url(r'^configuracion/trd/$', configuracion_views.config_trd),
        url(r'^configuracion/trd/modificacion/$', configuracion_views.config_trd_modificacion),
        url(r'^configuracion/trd/datos/$', configuracion_views.config_trd_datos),
        url(r'^configuracion/trd/dependencia/datos/$', configuracion_views.config_trd_dependencia_datos),
        url(r'^configuracion/trd/r_documentos/$', configuracion_views.config_trd_r_documentos),
        url(r'^configuracion/trd/sin_asignar/$', configuracion_views.config_trd_sin_asignar),
        url(r'^configuracion/trd/registrar/$', configuracion_views.config_trd_registrar),
        url(r'^configuracion/trd/informe/$', configuracion_views.config_trd_informa),


        #Ubicacion
        url(r'^configuracion/ubicacion/$', configuracion_views.config_ubicacion),
        url(r'^configuracion/ubicacion/registrar/$', configuracion_views.config_ubicacion_registrar),
        url(r'^configuracion/ubicacion/editar/(?P<id>[-\w]+)/$', configuracion_views.config_ubicacion_editar),

        #Piso
        url(r'^configuracion/piso/$', configuracion_views.config_piso),
        url(r'^configuracion/piso/registrar/$', configuracion_views.config_piso_registrar),
        #Salones
        url(r'^configuracion/salones/$', configuracion_views.config_salones),
        url(r'^configuracion/salones/registrar/$', configuracion_views.config_salones_registrar),
        #Estante
        url(r'^configuracion/estante/$', configuracion_views.config_estante),
        url(r'^configuracion/estante/registrar/$', configuracion_views.config_estante_registrar),
        #Nivel del estante
        url(r'^configuracion/nivel_estante/$', configuracion_views.config_nivel_estante),
        url(r'^configuracion/nivel_estante/registrar/$', configuracion_views.config_nivel_estante_registrar),

        #----------------------------------------VENTAS----------------------------------------------------------------------
        url(r'^configuracion/solicitud_pedido/$', configuracion_views.config_solicitud_pedido),
        url(r'^configuracion/solicitud_pedido/detalle/(?P<form_id>\d+)/$', configuracion_views.vista_formula),


        url(r'^configuracion/solicitud_entrega/$', configuracion_views.config_solicitud_entrega),
        url(r'^configuracion/solicitud_entrega/detalle/(?P<form_id>\d+)/$', configuracion_views.entrega_detalle),


        url(r'^configuracion/solicitud_devolucion/$', configuracion_views.config_solicitud_devolucion),
        url(r'^configuracion/solicitud_devolucion/detalle/(?P<form_id>\d+)/$', configuracion_views.devolucion_detalle),

        url(r'^configuracion/solicitud_notas_debito/$', configuracion_views.config_solicitud_notas_debito),
        url(r'^configuracion/solicitud_notas_debito/detalle/(?P<form_id>\d+)/$', configuracion_views.solicitud_notas_debito_detalle),


        url(r'^configuracion/solicitud_notas_credito/$', configuracion_views.config_solicitud_notas_credito),
        url(r'^configuracion/solicitud_notas_credito/detalle/(?P<form_id>\d+)/$', configuracion_views.solicitud_notas_credito_detalle),


        url(r'^configuracion/solicitud_factura_deudores/$', configuracion_views.config_solicitud_factura_deudores),
        url(r'^configuracion/solicitud_factura_deudores/detalle/(?P<form_id>\d+)/$', configuracion_views.factura_deudores_detalle),

        url(r'^configuracion/tarea/$', interlocutorc_views.tarea_api),

        url(r'^configuracion/solicitud_factura_proveedor/detalle/(?P<form_id>\d+)/$', configuracion_views.factura_deudores_proveedor),
        #---------------------------------------COMPRAS-------------------------------------------------------------------
        url(r'^configuracion/solicitud_pedido_orden/$', configuracion_views.config_solicitud_pedido_orden),
        url(r'^configuracion/solicitud_pedido_orden/bodegas/$', configuracion_views.config_solicitud_pedido_orden_bodega),
        url(r'^configuracion/solicitud_pedido_orden/detalle/(?P<form_id>\d+)/$', configuracion_views.pedido_detalle),
        url(r'^configuracion/solicitud_asignacion/pdf/(?P<form_id>\d+)/$', configuracion_views.pedido_asignacion_pdf),
        url(r'^configuracion/solicitud_pedido_orden/bodegas/detalle/(?P<form_id>\d+)/$', configuracion_views.pedido_detalle_bodega),
        url(r'^configuracion/solicitud_pedido_orden/bodegas/problema/(?P<form_id>\d+)/$', configuracion_views.pedido_problema_detalle_bodegas),
        url(r'^configuracion/solicitud_pedido_orden/bodegas/novedades/(?P<form_id>\d+)/(?P<novedad_id>\d+)/$', configuracion_views.pedido_problema_novedades_bodegas),
        url(r'^configuracion/solicitud_pedido_orden/problema/(?P<form_id>\d+)/$', configuracion_views.pedido_problema_detalle),
        url(r'^configuracion/solicitud_pedido_orden/novedades/(?P<form_id>\d+)/(?P<novedad_id>\d+)/$', configuracion_views.pedido_problema_novedades),
        url(r'^configuracion/solicitud_pedido_orden/cita_entrega/(?P<form_id>\d+)/(?P<novedad_id>\d+)/$', configuracion_views.pedido_problema_cita_entrega),
        url(r'^configuracion/solicitud_pedido_orden/excel/$', configuracion_views.reporte_pedido_detalle),
        url(r'^configuracion/solicitud_pedido_orden/excel_general/$', configuracion_views.reporte_pedido),
        url(r'^configuracion/solicitud_pedido_asignaciones_otroscanales/excel_general/$', configuracion_views.reporte_otroscanales),
        url(r'^configuracion/solicitud_pedido_cliente_otroscanales/excel_general/$', configuracion_views.reporte_otroscanales_cliente),
        url(r'^configuracion/solicitud_pedido_orden/excel_csv/$', configuracion_views.reporte_pedidos_csv),
        url(r'^configuracion/solicitud_pedido_orden/certificados_retencion/$', configuracion_views.reporte_certificados_retencion),

        url(r'^configuracion/solicitud_comprobante_egreso/excel/$', configuracion_views.reporte_comprobante_detalle),

        url(r'^configuracion/solicitud_catalogo_productos/$', configuracion_views.config_solicitud_catalogo_productos),
        url(r'^configuracion/solicitud_catalogo_productos/detalle/(?P<form_id>\d+)/$', configuracion_views.catalogo_productos_detalle),

        url(r'^configuracion/solicitud_debito_proveedores/$', configuracion_views.config_solicitud_debito_proveedores),
        url(r'^configuracion/solicitud_debito_proveedores/detalle/(?P<form_id>\d+)/$', configuracion_views.debito_proveedores_detalle),


        url(r'^configuracion/solicitud_credito_proveedores/$', configuracion_views.config_solicitud_credito_proveedores),
        url(r'^configuracion/solicitud_credito_proveedores/detalle/(?P<form_id>\d+)/$', configuracion_views.credito_proveedores_detalle),

        #---------------------------------------TABLAS NO SAP---------------------------------------------------------------
        url(r'^configuracion/solicitud_aviso_recibo/$', configuracion_views.config_solicitud_aviso_recibo),
        url(r'^configuracion/solicitud_aviso_recibo/excel_general/$', configuracion_views.reporte_aviso_recibo),

        url(r'^configuracion/solicitud_inventarios/$', configuracion_views.config_solicitud_inventarios),
        url(r'^configuracion/solicitud_inventarios/cliente/$', configuracion_views.config_solicitud_inventarios_cliente),
        url(r'^configuracion/solicitud_inventarios/excel_general/$', configuracion_views.reporte_inventario),
        url(r'^configuracion/solicitud_inventarios/detalle/$', configuracion_views.config_solicitud_inventarios_detalle),

        url(r'^configuracion/solicitud_ventas/$', configuracion_views.config_solicitud_ventas),
        url(r'^configuracion/solicitud_ventas/excel_general/$', configuracion_views.reporte_ventas),
        #---------------------------------------FINANZAS-------------------------------------------------------------------
        url(r'^configuracion/solicitud_pagos_recibidos/$', configuracion_views.config_solicitud_pagos_recibidos),
        url(r'^configuracion/solicitud_pagos_recibidos/detalle/(?P<form_id>\d+)/$', configuracion_views.pagos_recibidos_detalles),

        url(r'^configuracion/solicitud_estado_cuenta/$', configuracion_views.config_solicitud_estado_cuenta),
        url(r'^configuracion/solicitud_estado_cuenta/grupos/(?P<form_id>[\w\-]+)/$', configuracion_views.config_solicitud_estado_cuenta_grupos),
        url(r'^configuracion/solicitud_estado_cuenta/excel_general/$', configuracion_views.reporte_estado_cuenta),
        url(r'^configuracion/solicitud_estado_cuenta/detalle/(?P<form_id>[\w\-]+)/$', configuracion_views.estado_cuenta_detalle),
        url(r'^configuracion/solicitud_comprobante_egreso/$', configuracion_views.config_solicitud_comprobante_egreso),
        url(r'^configuracion/solicitud_comprobante_egreso/detalle/(?P<form_id>\d+)/$', configuracion_views.comprobante_egreso_detalles),
        url(r'^configuracion/solicitud_comprobante_egreso/print/(?P<form_id>\d+)/$', configuracion_views.comprobante_egreso_print),

        url(r'^configuracion/solicitud_comprobante_egreso_pcs/$', configuracion_views.config_solicitud_comprobante_egreso_pcs),
        #_______________________________________________ EXTERNO ____________________________________________________________

        # Login Referencia a  the 'django.contrib.auth.views.login' view to the /login/ URL.
        url(r'^login/$', interlocutorc_views.CustomLoginView.as_view(), name='login'),

        # Login Redirect
        url(r'^login-redirect/', interlocutorc_views.definir_login, name="login-redirect"),

        # Cerrar sesion Referencia  a 'django.contrib.auth.views.logout' view to the /logout/ URL.
        url(r'^logout/$', auth_views.logout,{"next_page": reverse_lazy('login')}, name="logout"),



    ]
)




urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)