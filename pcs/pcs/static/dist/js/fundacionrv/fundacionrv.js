

jQuery(document).ready(function($) {
    // Contact Form: Dynamic Select
    function select_changed(){
        $("div[id*='form-']").each(function(){
           $(this).removeClass('form-visible');
        });
        $("select[name='selectform']").each(function(){
            var selected = $(this).val();
            $('#'+selected).addClass('form-visible');
        });
    }

    $("select[name='selectform']").change(function(){
        select_changed();
    });
});


jQuery(document).ready(function($) {
  // Create Thumbnails
  $('.video-link').each(function(index, el) {
    $('#result').append('>>> ' + index + ':' + $(this).attr('data-source') + '<br>');
  });

  // Loading videos
  $('#gm-video-player video').on('loadstart', function (event) {
    $(this).addClass('loading');
  });
  $('#gm-video-player video').on('canplay', function (event) {
    $(this).removeClass('loading');
    $(this).attr('poster', '');
  });

  $('.video-link').on('click', function(event) {
    event.preventDefault();
    var video = $(this).attr('data-source');
    $('.video-link img').removeClass('video-active');
    $(this).find('img').addClass('video-active');
    createVideo(video);
  });
});

function createVideo (url) {
  var newVideo = '<video width="320" height="240" controls> <source src="'+url+'" type="video/mp4">';
  $('#gm-video-player').html(newVideo);
}

function createThumbnail (id) {
  var canvas = document.createElement('canvas');
  canvas.width = 160;
  canvas.height = 120;
  var context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
}

$(function () {

    // get csrf token cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // Iniciar Selects
    $(".select2").select2();

    // Iniciar Date picker
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        language: "es",
        autoclose: true
    });

    $('.datepicker').datepicker('update', new Date());

    // Iniciar datatables
     $(".dataTables").DataTable({
        language: {
            url: spanish_json
        },
        "aaSorting":[]
     });

     // Iniciar datatables simple
     $(".dataTableSimple").DataTable({
        language: {
            url: spanish_json
        },
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
        "aaSorting":[]
     });

    console.log("Entre al document.onLoad()");



    //------------------------------------- REPORTES EN PANTALLA ------------------------------------------


    //BUSCAR TIPOS DE DOCUMENTOS X SUBSERIE Y SOPORTE
    var buscar_tipos_documentos_trd = function () {

        subseries = $("#subseries").val() || "";
        subseries = subseries.replace(/\s+/g, '');
        soporte = $("#soporte").val() || "";
        soporte = soporte.replace(/\s+/g, '');
        dependencias = $("#dependencias").val() || "";
        dependencias = dependencias.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/trd/r_documentos/?subseries='+subseries+'&soporte='+soporte+'&dependencias='+dependencias,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        matriz = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_documentos_asignados tbody")
                        table_body.empty();
                        for(var i=0;i<matriz.length; i++)
                               {
                                lineas +=   "<tr>" +

                                            "<td>"+matriz[i].codigo+"</td>" +
                                            "<td>"+matriz[i].descripcion+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_documentos_asignados_input").click(
       function (e) {
           buscar_tipos_documentos_trd()
       }
    )

    $("#subseries").change(
       function (e) {
           buscar_tipos_documentos_no_trd()
       }
    )

    $("#soporte").change(
       function (e) {
           buscar_tipos_documentos_no_trd()
       }
    )

    $("#dependencias").change(
       function (e) {
           buscar_tipos_documentos_no_trd()
       }
    )

    //BUSCAR TIPOS DE DOCUMENTOS NO ASIGNADOS X SUBSERIE Y SOPORTE
    var buscar_tipos_documentos_no_trd = function () {

        subseries = $("#subseries").val() || "";
        subseries = subseries.replace(/\s+/g, '');
        soporte = $("#soporte").val() || "";
        soporte = soporte.replace(/\s+/g, '');
        dependencias = $("#dependencias").val() || "";
        dependencias = dependencias.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/trd/sin_asignar/?subseries='+subseries+'&soporte='+soporte+'&dependencias='+dependencias,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        matriz = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_documento_sin_asignar tbody")
                        table_body.empty();
                        for(var i=0;i<matriz.length; i++)
                               {
                                lineas +=   "<tr>" +

                                            "<td>"+matriz[i].id+"</td>" +
                                            "<td>"+matriz[i].descripcion+"</td>" +
                                            "<td>"+"<input type='checkbox' id='tipo_documento' name='tipo_documento[]' value=' "
                                            +matriz[i].id+"'"+"</td>" +
                                    "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }


    //BUSCAR SOLICITUD X DEPENDENCIA Y TIPO RADICACION

    var buscar_solicitud_dependencia_radicado = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        tipo_radicado = $("#tipo_radicado").val() || "";
        tipo_radicado = tipo_radicado.replace(/\s+/g, '');
        dependencia = $("#dependencia").val() || "";
        dependencia = dependencia.replace(/\s+/g, '');


        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/admin_anulacion/r_solicitud/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&tipo_radicado='+tipo_radicado+'&dependencia='+dependencia,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        solicitud = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_solicitudes_anulacion tbody")
                        table_body.empty();
                        for(var i=0;i<solicitud.length; i++)
                               {
                                lineas +=   "<tr>" +
                                            "<td>"+solicitud[i].dependencia+"</td>" +
                                            "<td>"+solicitud[i].radicado+"</td>" +
                                            "<td>"+solicitud[i].fecha +
                                            "<td>"+solicitud[i].observacion+"</td>" +

                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_solicitud_dependencia_input").click(
       function (e) {
           buscar_solicitud_dependencia_radicado()
       }
    )




                                     //BUSCAR PACIENTES X CEDULA

    var buscar_paciente_cedula = function () {

        valor_ingresado = $("#busqueda_paciente_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?identificacion_personal='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                           {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
                        registrar_borrado($(".borrar_paciente_button"),'PACIENTE')
    }
    });
    }

    $("#busqueda_paciente_button").click(
       function (e) {
           buscar_paciente_cedula()
       }
    )

                                     //BUSCAR PACIENTES X NOMBRES

    var buscar_paciente_nombres = function () {

        valor_ingresado = $("#busqueda_paciente_nombre_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?identificacion_personal='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                           {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='borrar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
                        registrar_borrado($(".borrar_paciente_button"),'PACIENTE')
    }
    });
    }

    $("#busqueda_paciente_nombre_button").click(
       function (e) {
           buscar_paciente_nombres()
       }
    )

                                         //BUSCAR CASOS X CEDULA

    var buscar_casos_pacientes_cedula = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_cedula_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?paciente_id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        var lineas = ''
                        var estado = ''
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                "<button>"+
                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                "</span>"+
                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                "</a>"+
                                            "</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                    "</span>"+ "Notificación"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-random'>"+
                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/informacion_complementaria/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-file'>"+
                                                    "</span>"+ "Info. Complementaria"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                "<button id='modificar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/borrar/'>" +
                                                "<button id='borrar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-trash'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "</td>"+
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        registrar_borrado($(".borrar_caso_button"),'CASO')
    }
    });
    };

    $("#busqueda_casos_pacientes_cedula_button").click(
       function (e) {
           buscar_casos_pacientes_cedula()
       }
    );

                                            //BUSCAR CASOS X NOMBRES

    var buscar_casos_pacientes_nombres = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_nombres_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?paciente_id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody");
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                "<button>"+
                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                "</span>"+
                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                "</a>"+
                                            "</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                    "</span>"+ "Notificación"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-random'>"+
                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/informacion_complementaria/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-file'>"+
                                                    "</span>"+ "Info. Complementaria"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                "<button id='modificar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/borrar/'>" +
                                                "<button id='borrar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-trash'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "</td>"+
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        registrar_borrado($(".borrar_caso_button"),'CASO')
    }
    });
    }

    $("#busqueda_casos_pacientes_nombres_button").click(
       function (e) {
           buscar_casos_pacientes_nombres()
       }
    )

                                           //BUSCAR CASOS X REGIMEN

    var buscar_casos_pacientes_regimen = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_regimen_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?regimen_id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1
                        var lineas = ''
                        var estado = ''
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                "<button>"+
                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                "</span>"+
                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                "</a>"+
                                            "</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                    "</span>"+ "Notificación"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-random'>"+
                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                "<button id='modificar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/borrar/'>" +
                                                "<button id='borrar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-trash'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "</td>"+
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_regimen_button").click(
       function (e) {
           buscar_casos_pacientes_regimen()
       }
    )

    //BUSCAR CASOS X ESTADO

    var buscar_casos_pacientes_estado = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_estado_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?estado_id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1
                        var lineas = ''
                        var estado = ''
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                "<button>"+
                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                "</span>"+
                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                "</a>"+
                                            "</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                    "</span>"+ "Notificación"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-random'>"+
                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                "<button id='modificar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/borrar/'>" +
                                                "<button id='borrar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-trash'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "</td>"+
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_estado_button").click(
       function (e) {
           buscar_casos_pacientes_estado()
       }
    )

                                        //BUSCAR CASOS X EPS

    var buscar_casos_pacientes_eps = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_eps_input").val() || "";
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?eps_id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        var lineas = '';
                        var table_body = $("#tabla_casos_pacientes tbody");
                        table_body.empty();
                        $.ajax({
                                type: "GET",
                                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                                url: '/usuarios/pacientes/rcasos/?eps_id='+valor_ingresado,
                                dataType:'json',
                                success: function(data) {
                                    // Cargar en tabla
                                        casos = data.datos;
                                        contador = 1;
                                        var lineas = '';
                                        var estado = '';
                                        var table_body = $("#tabla_casos_pacientes tbody");
                                        table_body.empty();
                                        for(var i=0;i<casos.length; i++)
                                               {

                                                if (casos[i].estado === 'PENDIENTE') {
                                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                                if (casos[i].estado === 'EN PROCESO') {
                                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                                if (casos[i].estado === 'FINALIZADO') {
                                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                                lineas +=   "<tr>" +
                                                            "<td>"+(contador++)+"</td>" +
                                                            "<td>"+casos[i].id+"</td>" +
                                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                                            "<td>"+casos[i].enfermedad+"</td>" +
                                                            "<td>"+casos[i].eps+"</td>" +
                                                            "<td>"+casos[i].regimen+"</td>" +
                                                            estado+
                                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                                            "<td>" +
                                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                                "<button>"+
                                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                                "</span>"+
                                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                                "</a>"+
                                                            "</td>" +
                                                            "<td>" +
                                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                                    "<button>"+
                                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                                    "</span>"+ "Notificación"+ "</button>"+
                                                                    "</a>"+
                                                            "</td>"+
                                                            "<td>" +
                                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                                    "<button>"+
                                                                    "<span class='glyphicon glyphicon-random'>"+
                                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                                    "</a>"+
                                                            "</td>"+
                                                            "<td>"+
                                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                                "<button id='modificar_caso_button'>"+
                                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                                "</span>"+ "</button>"+
                                                            "</a>"+
                                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/borrar/'>" +
                                                                "<button id='borrar_caso_button'>"+
                                                                "<span class='glyphicon glyphicon-trash'>"+
                                                                "</span>"+ "</button>"+
                                                            "</a>"+
                                                            "</td>"+
                                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
                        table_body.append(lineas)
    }
    });
    };

    $("#busqueda_casos_pacientes_eps_button").click(
       function (e) {
           buscar_casos_pacientes_eps()
       }
    )

                                     //BUSCAR PACIENTES X CANAL_INVITACION

    var buscar_paciente_canal_invitacion = function () {

        valor_ingresado = $("#busqueda_pacientes_canal_invitacion_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?canal_invitacion='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                           {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+ pacientes[i].canal_invitacion + "</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='borrar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_pacientes_canal_invitacion_button").click(
       function (e) {
           buscar_paciente_canal_invitacion()
       }
    )


                                 //BUSCAR PACIENTES X DEPARTAMENTO

    var buscar_paciente_departamento= function () {

        valor_ingresado = $("#busqueda_pacientes_departamento_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?departamento='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = '';
                        var table_body = $("#tabla_pacientes tbody");
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                          {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='borrar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_pacientes_departamento_button").click(
       function (e) {
           buscar_paciente_departamento()
       }
    )

                                    //BUSCAR PACIENTES X DEPARTAMENTO

    var buscar_paciente_municipio = function () {

        valor_ingresado = $("#busqueda_pacientes_municipio_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?municipio='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                           {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='borrar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_pacientes_municipio_button").click(
       function (e) {
           buscar_paciente_municipio()
       }
    )

                                      //BUSCAR PACIENTES X SEXO

    var buscar_paciente_sexo = function () {

        valor_ingresado = $("#busqueda_pacientes_sexo_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rpaciente/?sexo='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        pacientes = data.datos;
                        var lineas = '';
                        var table_body = $("#tabla_pacientes tbody");
                        table_body.empty();
                        for(var i=0;i<pacientes.length; i++)
                           {
                            lineas +=
                                "<tr>" +
                                    "<td>"+ pacientes[i].tipo_identificacion + " : " +  pacientes[i].identificacion_personal+"</td>" +
                                    "<td>"+ pacientes[i].nombre_uno + "<br>"
                                          + pacientes[i].nombre_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].apellido_uno + "<br>"
                                          + pacientes[i].apellido_dos +
                                    "</td>" +
                                    "<td>"+ pacientes[i].direccion_residencia + "<br>"
                                          + pacientes[i].id_municipio + " , " + pacientes[i].id_departamento + "<br>"
                                          + pacientes[i].id_pais +
                                    "</td>" +
                                    "<td>"+ pacientes[i].telefonos + "</td>" +
                                    "<td>"+ pacientes[i].email_personal + "</td>" +
                                    "<td>"+pacientes[i].sexo+"</td>" +
                                    "<td>"+pacientes[i].edad+"</td>" +
                                    "<td>" +
                                        "<a href='/administracion/pacientes/casos/?cedula="+pacientes[i].identificacion_personal+"'>" +
                                            "<button>"+
                                            "<span class='glyphicon glyphicon-folder-open'>"+
                                            "</span>"+
                                            "<span class='glyphicon glyphicon-zoom-in'>"+
                                            "</span>"+
                                            "<br>"+ " Detalle_Casos"+ "</button>"+
                                            "</a>"+
                                    "</td>" +
                                    "<td>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/detalle/'>" +
                                        "<button id='modificar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-pencil'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                        "<button id='borrar_paciente_button'>"+
                                        "<span class='glyphicon glyphicon-trash'>"+
                                        "</span>"+ "</button>"+
                                    "</a>"+
                                    "</td>"+
                                "</tr>";
                           }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_pacientes_sexo_button").click(
       function (e) {
           buscar_paciente_sexo()
       }
    )

    var buscar_casos_pacientes_enfermedad = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_enfermedad_input").val() || ""


        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?enfermedad='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody");
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/?cedula="+casos[i].indetificacion_paciente+"'>" +
                                                "<button>"+
                                                "<span class='glyphicon glyphicon-folder-open'>"+
                                                "</span>"+
                                                "<span class='glyphicon glyphicon-zoom-in'>"+
                                                "</span>"+ "Detalle_Casos"+ "</button>"+
                                                "</a>"+
                                            "</td>" +
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/notificacion/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-envelope'>"+
                                                    "</span>"+ "Notificación"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>" +
                                                "<a href='/administracion/pacientes/casos/seguimiento/?id="+casos[i].id+"'>" +
                                                    "<button>"+
                                                    "<span class='glyphicon glyphicon-random'>"+
                                                    "</span>"+ "Seguimiento	"+ "</button>"+
                                                    "</a>"+
                                            "</td>"+
                                            "<td>"+
                                            "<a href='/usuarios/pacientes/casos/"+casos[i].id+"/detalle/'>" +
                                                "<button id='modificar_caso_button'>"+
                                                "<span class='glyphicon glyphicon-pencil'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "<a href='/usuarios/pacientes/paciente/"+pacientes[i].identificacion_personal+"/borrar/'>" +
                                                "<button id='borrar_paciente_button'>"+
                                                "<span class='glyphicon glyphicon-trash'>"+
                                                "</span>"+ "</button>"+
                                            "</a>"+
                                            "</td>"+
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_enfermedad_button").click(
       function (e) {
           buscar_casos_pacientes_enfermedad()
       }
    )


    //------------------------------------------- REPORTES POR FECHAS--------------------------------------------------

       //BUSCAR CASOS X ESTADO Y FECHA

    var buscar_casos_pacientes_fecha_estado = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_estado_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_estado()
       }
    )

    //BUSCAR CASOS X EPS Y FECHA

    var buscar_casos_pacientes_fecha_eps = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        eps = $("#eps_input").val() || "";
        eps = eps.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');


        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_eps='+eps+'&r_estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                               {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_eps_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_eps()
       }
    )

    //BUSCAR CASOS X DIAGNOSTICO Y FECHA

    var buscar_casos_pacientes_fecha_enfermedad = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        enfermedad = $("#enfermedad_input").val() || "";
        enfermedad = enfermedad.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_enfermedad='+enfermedad,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_enfermedad_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_enfermedad()
       }
    )

    //BUSCAR CASOS X DEPARTAMENTO Y FECHA

    var buscar_casos_pacientes_fecha_departamento = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        departamento = $("#departamento_input").val() || "";
        departamento = departamento.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_departamento='+departamento,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_departamento_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_departamento()
       }
    )

    //BUSCAR CASOS X MUNICIPIO Y FECHA

    var buscar_casos_pacientes_fecha_municipio = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        municipio = $("#municipio_input").val() || "";
        municipio = municipio.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_municipio='+municipio,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                              {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_municipio_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_municipio()
       }
    )

    //BUSCAR CASOS X MEDICAMENTO REGISTRADO EN LA FORMULA MEDICA Y FECHA

    var buscar_casos_pacientes_fecha_medicamento = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        medicamento = $("#medicamento_input").val() || "";
        medicamento = medicamento.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/administracion/pacientes/formula/rmedicamentos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'r_medicamento='+medicamento,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_pacientes_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }


    $("#busqueda_casos_pacientes_fecha_medicamento_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_medicamento()
       }
    )


    //BUSCAR CASOS X MUNICIPIO Y FECHA

    var buscar_casos_pacientes_fecha_municipio = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        municipio = $("#municipio_input").val() || "";
        municipio = municipio.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/usuarios/pacientes/rcasos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&r_municipio='+municipio,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_casos_pacientes tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                              {

                                if (casos[i].estado === 'PENDIENTE') {
                                estado="<td style='color:#dd4b39'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'EN PROCESO') {
                                estado="<td style='color:#f5841f'>"+casos[i].estado+"</td>";}

                                if (casos[i].estado === 'FINALIZADO') {
                                estado="<td style='color:#50bc37'>"+casos[i].estado+"</td>";}

                                lineas +=   "<tr>" +
                                            "<td>"+(contador++)+"</td>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].indetificacion_paciente+"</td>" +
                                            "<td>"+ casos[i].nombre_uno + "<br>"
                                                  + casos[i].nombre_dos +
                                            "</td>" +
                                            "<td>"+ casos[i].apellido_uno + "<br>"
                                                  + casos[i].apellido_dos +
                                            "</td>" +
                                            "<td>"+casos[i].telefonos+"</td>" +
                                            "<td>"+casos[i].enfermedad+"</td>" +
                                            "<td>"+casos[i].eps+"</td>" +
                                            "<td>"+casos[i].regimen+"</td>" +
                                            "<td>"+casos[i].barreras+"</td>" +
                                            estado+
                                            "<td>"+casos[i].fecha_solicitudrv+"</td>"+
                                            "<td>"+casos[i].fecha_enproceso_caso+"</td>" +
                                            "<td>"+casos[i].fecha_finalizacion_caso+"</td>" +
                                            "<td>"+casos[i].tiempo_respuesta+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }

    $("#busqueda_casos_pacientes_fecha_municipio_button").click(
       function (e) {
           buscar_casos_pacientes_fecha_municipio()
       }
    )

    //BUSCAR SOLICITUDES GENERALES

    var buscar_infoc_solicitudes = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        peticiones = $("#peticiones_input").val() || "";
        peticiones = peticiones.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');
        grupo = $("#grupo_input").val() || "";
        grupo = grupo.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/solicitudes_generales/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&peticiones='+peticiones+'&estado='+estado+'&grupo='+grupo,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].id+"</td>" +
                                            "<td>"+casos[i].empresa+"</td>" +
                                            "<td>"+ casos[i].num_pedido +
                                            "</td>" +
                                            "<td>"+ casos[i].peticion +
                                            "</td>" +
                                            "<td>"+casos[i].fecha+"</td>" +
                                            "<td>"+casos[i].estado+"</td>" +
                                            "<td> <a class='btn btn-info' href='/configuracion/solicitud_pedido_orden/problema/"+ casos[i].entry_pedido +
                                            "'><i class='fa fa-mail-forward'></i></a> </td>"+

                                            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }


    $("#busqueda_solicitudes_generales").click(
       function (e) {
           buscar_infoc_solicitudes()
       }
    )



    //BUSCAR CREDITOS CREDIYA

    var buscar_crediya_solicitudes = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        empresa = $("#empresa_input").val() || "";
        empresa = empresa.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/servicio_crediya_consulta/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa='+empresa+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].empresa+"</td>" +
                                            "<td>"+ casos[i].pedido +
                                            "<td>"+ casos[i].almacen +
                                            "<td>"+ casos[i].fecha_solicitud +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha +
                                            "</td>" +
                                            "<td>"+ casos[i].vencimiento +
                                            "</td>" +
                                            "<td>"+ casos[i].valor_preaprobado +
                                            "</td>" +
                                            "<td>"+casos[i].interes+"</td>" ;
                                            if (casos[i].estado === 'Preaprobado') {
                                                lineas += "<td><div class=\"btn-group\"> "
                                                            +"<button type=\"button\" class=\"btn btn-btn btn-success aceptar-btn\" " +
                                                    "data-pedido='"+ casos[i].pedido +"' data-toggle='modal' data-target='#AceptarCredito'>ACEPTAR</button>"
                                                            +"<button type=\"button\" class=\"btn btn-btn btn-danger denegar-btn\" " +
                                                    "data-pedido='"+ casos[i].pedido +"' data-toggle='modal' data-target='#DenegarCredito'>DENEGAR</button>"
                                                            +"</div></td>";

                                            } else if (casos[i].estado === 'Aprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-success\">Aprobado</span></td>";}
                                            else{
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-danger\">Negado</span></td>";
                                            }
                                lineas+=
                                            "<td>"+casos[i].usuario_aprobacion+"</td>" +
                                            "<td>"+casos[i].fecha_aprobacion+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        $(".aceptar-btn").click(function () {
                            var pedido = $(this).data("pedido");
                            $("#pedido_modal").text(pedido);
                            $("#numeropedido1").val(pedido);
                        });
                        $(".denegar-btn").click(function () {
                            var pedido = $(this).data("pedido");
                            $("#pedido_modal2").text(pedido);
                            $("#numeropedido2").val(pedido);
                        });
    }
    });
    }


    $("#busqueda_solicitudes_crediya").click(
       function (e) {
           buscar_crediya_solicitudes()
       }
    )


    $(document).ready(function () {
        $(".aceptar-btn").click(function () {
            var pedido = $(this).data("pedido");
            $("#pedido_modal").text(pedido);
            $("#numeropedido1").val(pedido);
        });
        $(".denegar-btn").click(function () {
            var pedido = $(this).data("pedido");
            $("#pedido_modal2").text(pedido);
            $("#numeropedido2").val(pedido);
        });
    });







     //BUSCAR CREDITOS CREDILISTO

    var buscar_credilisto_solicitudes = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        empresa = $("#empresa_input").val() || "";
        empresa = empresa.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/servicio_credilisto_consulta/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa='+empresa+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].empresa+"</td>" +
                                            "<td>"+ casos[i].factura +
                                            "<td>"+ casos[i].facturacliente +
                                            "<td>"+ casos[i].fechafactura +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha +
                                            "</td>" +
                                            "<td>"+ casos[i].vencimiento +
                                            "</td>" +
                                            "<td>"+ casos[i].valor_preaprobado +
                                            "</td>" +
                                            "<td>"+casos[i].interes+"</td>" +
                                            "<td>"+casos[i].interes_aplicado+"</td>";
                                            if (casos[i].estado === 'Preaprobado') {
                                                lineas += "<td><div class=\"btn-group\"> "
                                                            +"<button type=\"button\" class=\"btn btn-btn btn-success aceptarcredi-btn\" " +
                                                    "data-pedido='"+ casos[i].factura +"' data-toggle='modal' data-target='#AceptarCredito'>ACEPTAR</button>"
                                                            +"<button type=\"button\" class=\"btn btn-btn btn-danger denegarcredi-btn\" " +
                                                    "data-pedido='"+ casos[i].factura +"' data-toggle='modal' data-target='#DenegarCredito'>DENEGAR</button>"
                                                            +"</div></td>";

                                            } else if (casos[i].estado === 'Aprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-success\">Aprobado</span></td>";}
                                            else{
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-danger\">Negado</span></td>";
                                            }
                                lineas+=
                                            "<td>"+casos[i].usuario_aprobacion+"</td>" +
                                            "<td>"+casos[i].fecha_aprobacion+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        $(".aceptarcredi-btn").click(function () {
                            var pedido = $(this).data("pedido");
                            $("#pedido_modal").text(pedido);
                            $("#PedidosCruzados").text('ESPERE UN MOMENTO POR FAVOR');
                            $("#numeropedido1").val(pedido);
                            $.ajax({
                                url: '/configuracion/servicio_credilisto_consulta/cruces/',
                                method: 'GET',
                                data: {pedido: pedido},
                                success: function(response) {
                                    $("#PedidosCruzados").text(response.resultado);
                                    $("#estado").val(response.estado);
                                    $("#pedido_sap").val(response.pedido);
                                    $("#valor_sap").val(response.valor);
                                    },
                                error: function(xhr, status, error) {
                                    console.error(xhr.responseText);
                                }
                            });
                        });
                        $(".denegarcredi-btn").click(function () {
                            var pedido = $(this).data("pedido");
                            $("#pedido_modal2").text(pedido);
                            $("#numeropedido2").val(pedido);
                        });
    }
    });
    }


    $("#busqueda_solicitudes_credilisto").click(
       function (e) {
           buscar_credilisto_solicitudes()
       }
    )

    $(document).ready(function () {
    $(".aceptarcredi-btn").click(function () {
    var pedido = $(this).data("pedido");
    $("#pedido_modal").text(pedido);
    $("#AprobarCreditoBtn").prop("disabled", true);
    $("#PedidosCruzados").text('ESPERE UN MOMENTO POR FAVOR');
    $("#numeropedido1").val(pedido);

    // Limpiar tabla anterior si existe
    $("#tablaPendientesContainer").empty();

    $.ajax({
        url: '/configuracion/servicio_credilisto_consulta/cruces/',
        method: 'GET',
        data: {pedido: pedido},
        success: function(response) {
            $("#PedidosCruzados").text(response.resultado);
            $("#estado").val(response.estado);
            $("#pedido_sap").val(response.pedido);
            $("#valor_sap").val(response.valor);
            $("#AprobarCreditoBtn").prop("disabled", false);

            // Si hay datos en consulta_pendientes, los mostramos como tabla
            if (response.consulta_pendientes && response.consulta_pendientes.length > 0) {
                var tablaHTML = `
                    <table class="table table-bordered table-hover">
                        <thead>
                            <tr>
                                <th>Seleccionar <input type="checkbox" id="seleccionar_todo_modal"></th>
                                <th>Tipo</th>
                                <th>Descripción</th>
                                <th>Saldo</th>
                                <th>Origen</th>
                                <th>Fecha</th>
                            </tr>
                        </thead>
                        <tbody>`;

                response.consulta_pendientes.forEach(function(item, index) {
                    let rowId = `fila_${index}`;

                    // --- Formatear fecha YYYYMMDD -> DD/MM/YYYY ---
                    let fechaFormateada = "";
                    if (item.fecha && item.fecha.length === 8) {
                        fechaFormateada = item.fecha.substring(6, 8) + "/" +
                                          item.fecha.substring(4, 6) + "/" +
                                          item.fecha.substring(0, 4);
                    }

                    tablaHTML += `
                        <tr id="${rowId}">
                            <td>
                                <input type="checkbox" class="check-pendiente" 
                                    name="pendientes_seleccionados[]" 
                                    data-index="${index}"
                                    value="${item.tipo},${item.descripcion},${item.saldo},${item.origen},${item.entry}">
                            </td>
                            <td>${item.tipo}</td>
                            <td>${item.descripcion}</td>
                            <td>
                                <input type="number" class="form-control saldo-input" 
                                    data-index="${index}" 
                                    value="${item.saldo}" 
                                    max="${item.saldo}">
                            </td>
                            <td>${item.origen}</td>
                            <td>${fechaFormateada}</td>
                        </tr>`;
                });

                tablaHTML += `</tbody></table>`;
                $("#tablaPendientesContainer").html(tablaHTML);

                // Seleccionar todos
                $(document).off('change', '#seleccionar_todo_modal').on('change', '#seleccionar_todo_modal', function () {
                    var checked = this.checked;
                    $("#tablaPendientesContainer input[type='checkbox'].check-pendiente").prop('checked', checked);
                });

                // Actualizar el valor del checkbox cuando cambia el saldo
                $(document).off('input', '.saldo-input').on('input', '.saldo-input', function () {
                    var index = $(this).data('index');
                    var nuevoSaldo = $(this).val();
                    var checkbox = $(`input.check-pendiente[data-index='${index}']`);
                    var partes = checkbox.val().split(',');
                    partes[2] = nuevoSaldo; // Reemplazamos el saldo
                    checkbox.val(partes.join(','));
                });
            }
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
});

    $(".denegarcredi-btn").click(function () {
        var pedido = $(this).data("pedido");
        $("#pedido_modal2").text(pedido);
        $("#numeropedido2").val(pedido);
    });
});


    $(document).ready(function () {
        $(".aceptardocumentos-btn").click(function () {
            var id = $(this).data("id");
            $("#numerosoli").val(id);
        });
        $(".denegardocumentos-btn").click(function () {
            var id = $(this).data("id");
            $("#numerosolis").val(id);
        });
    });


 //BUSCAR CREDITOS CREDIYA EMPRESARIO

    var buscar_crediya_historiales = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/servicio_crediya_historial/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].empresa+"</td>" +
                                            "<td>"+ casos[i].pedido +
                                            "<td>"+ casos[i].fecha_solicitud +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha_vencimiento +
                                            "</td>" +
                                            "<td>"+ casos[i].valor_preaprobado +
                                            "</td>" +
                                            "<td>"+casos[i].interes+"</td>" ;
                                            if (casos[i].estado === 'Preaprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-info\">PreAprobado</span></td><td></td>";

                                            } else if (casos[i].estado === 'Aprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-success\">Aprobado</span></td><td></td>";}
                                            else{
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-danger\">Negado</span></td>"+
                                                "<td><button type=\"button\" class=\"btn btn-primary razon-btn\"\n" +
                                                    "data-razon='"+ casos[i].razon + "' data-toggle=\"modal\" data-dismiss=\"modal\"\n" +
                                                    "data-target=\"#RazonNegado\">RESPUESTA</button></td>";
                                            }
                                lineas+=
                                            "<td>"+casos[i].fecha_aprobado+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        $(".razon-btn").click(function () {
                            var razon = $(this).data("razon");
                            $("#razonnegado").text(razon);
                        });
    }
    });
    }


    $("#busqueda_historiales_crediya").click(
       function (e) {
           buscar_crediya_historiales()
       }
    )





     //BUSCAR CREDITOS CREDILISTO EMPRESARIO

    var buscar_credilisto_historiales = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/servicio_credilisto_historial/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td>"+casos[i].empresa+"</td>" +
                                            "<td>"+ casos[i].pedido +
                                            "<td>"+casos[i].factura_cliente+"</td>" +
                                            "<td>"+ casos[i].fecha_solicitud +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha +
                                            "</td>" +
                                            "<td>"+ casos[i].fecha_vencimiento +
                                            "</td>" +
                                            "<td>"+ casos[i].valor_preaprobado +
                                            "</td>" +
                                            "<td>"+casos[i].interes+"</td>"+
                                            "<td>"+casos[i].interesapl+"</td>" ;
                                            if (casos[i].estado === 'Preaprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-info\">PreAprobado</span></td><td></td>";

                                            } else if (casos[i].estado === 'Aprobado') {
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-success\">Aprobado</span></td><td></td>";}
                                            else{
                                                lineas +="<td> <span style=\"font-weight: bold;font-size: 1.2em\" class=\"label label-danger\">Negado</span></td>"+
                                                "<td><button type=\"button\" class=\"btn btn-primary razon-btn\"\n" +
                                                    "data-razon='"+ casos[i].razon + "' data-toggle=\"modal\" data-dismiss=\"modal\"\n" +
                                                    "data-target=\"#RazonNegado\">RESPUESTA</button></td>";
                                            }
                                lineas+=
                                            "<td>"+casos[i].fecha_aprobado+"</td>" +
                                            "</tr>";
                               }
                        table_body.append(lineas)
                        $(".razon-btn").click(function () {
                            var razon = $(this).data("razon");
                            $("#razonnegado").text(razon);
                        });
    }
    });
    }


    $("#busqueda_historiales_credilisto").click(
       function (e) {
           buscar_credilisto_historiales()
       }
    )




    //CALCULAR VALORES CREDIYA
    $(document).ready(function () {
        $('.solicitud-btn').click(function () {
            $("#mensajeConfirmacion").hide();
            $("#solicitarCreditoBtn").show();
            var pedidoId = $(this).data('id');
            var pedidoPedido = $(this).data('pedido');
            var pedidoFecha = $(this).data('fecha');
            var pedidoVencimiento = $(this).data('vencimiento');
            var pedidoAlmacen = $(this).data('almacen');
            $.ajax({
                url: '/configuracion/servicio_crediya_lista/',
                method: 'GET',
                data: { pedido_id: pedidoId },
                success: function (data) {
                    $('#numeroPedido').text(pedidoPedido);
                    $('#numeroPedido1').val(pedidoPedido);
                    $('#fecha_pedido').val(pedidoFecha);
                    $('#desembolso').text(data.valor1);
                    $('#desembolso1').val(data.valor1);
                    $('#intereses').text(data.valor2);
                    $('#intereses1').val(data.valor2);
                    $('#desembolsos').text(data.valor3);
                    $('#desembolsos1').val(data.valor3);
                    $('#valor_orden').val(pedidoId);
                    $('#fecha_vencimiento').val(pedidoVencimiento);
                    $('#pedido_almacen').val(pedidoAlmacen);
                }
            });
        });
    });




$(document).ready(function () {
    $('#generarSeleccionados').on('click', function () {
        let pedidosSeleccionados = [];

        $('.pedido-checkbox:checked').each(function () {
            pedidosSeleccionados.push($(this).val());
        });

        if (pedidosSeleccionados.length === 0) {
            alert('Debe seleccionar al menos un pedido.');
            $('#DocumentoFIModal').modal('hide');
            return;
        }

        // Insertar lista en input oculto (separado por comas)
        $('#numero_pedidoss').val(pedidosSeleccionados.join(','));
    });
});


    //CALCULAR VALORES CREDILISTO
    $(document).ready(function () {
        $('.solicitud-credilisto-btn').click(function () {
            $("#mensajeConfirmacion").hide();
            $("#solicitarCreditoBtn").show();
            var facturaId = $(this).data('id');
            var facturaFactura = $(this).data('factura');
            var facturaFecha = $(this).data('fecha');
            var facturaVencimiento = $(this).data('vencimiento');
            var facturaReferencia = $(this).data('referencia');
            $.ajax({
                url: '/configuracion/servicio_credilisto_lista/',
                method: 'GET',
                data: { factura_id: facturaId , factura_vencimiento: facturaVencimiento },
                success: function (data) {
                    $('#numeroFactura').text(facturaFactura);
                    $('#numeroFacturaCliente').text(facturaReferencia);
                    $('#interescre').text(data.valor2);
                    $('#ochentaporciento').text(data.valor3);
                    $('#diferencia').text(data.diferencia);
                    $('#desembolsocredi').text(data.valor1);
                    $('#numeroPedido1').val(facturaFactura);
                    $('#intereses1').val(data.valor2);
                    $('#desembolso1').val(data.valor1);
                    $('#fecha_pedido').val(facturaFecha);
                    $('#valor_orden').val(facturaId);
                    $('#fecha_vencimiento').val(facturaVencimiento);
                    $('#factura_cliente').val(facturaReferencia);
                }
            });
        });
    });



    //CALCULAR VALORES CODIGO
    $(document).ready(function () {
        $('.solicitud-codigoregistro-btn').click(function () {
            var facturaReferencia = 1;
            $.ajax({
                url: '/configuracion/servicio_codigo_registro_lista/',
                method: 'GET',
                data: { factura_id: facturaReferencia  },
                success: function (data) {
                    $('#numerocodigo').text(data.valor1);
                    $('#numerocodigos').val(data.valor1);
                }
            });
        });
    });



    //BUSCAR PEDIDOS OTROS CANALES
        var busqueda_pedidos_otros_canales = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        empresa = $("#empresa_input").val() || "";
        empresa = empresa.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/pedidos_otros_canales/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa='+empresa+'&pedido='+pedido+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
for (var i = 0; i < casos.length; i++) {
    lineas += "<tr>";

    // Checkbox
    lineas += "<td><input type='checkbox' class='pedido-checkbox' value='" + casos[i].num_pedido + "'></td>";

    // Datos del pedido
    lineas += "<td>Pedido #" + casos[i].num_pedido + "</td>";
    lineas += "<td>" + (casos[i].num_pedido_CLI || "") + "</td>";
    lineas += "<td>" + (casos[i].fecha || "") + "</td>";
    lineas += "<td>" + (casos[i].fecha_entrega || "") + "</td>";
    lineas += "<td>" + (casos[i].hora || "") + "</td>";

    // Estado con estilos
    if (casos[i].estado === 'en proceso') {
        lineas += "<td><span class='label label-info'>" + casos[i].estado + "</span></td>";
    } else {
        lineas += "<td><span class='label label-primary'>" + casos[i].estado + "</span></td>";
    }

    // Botón de detalles
    lineas += "<td><a class='btn btn-info' href='/configuracion/orden_pcs_otroscanales/detalle/" + casos[i].num_pedido + "'><i class='fa fa-mail-forward'></i></a></td>";

    lineas += "</tr>";
}

// Añadir al DOM
table_body.append(lineas);
    }
    });
    }


    $("#busqueda_pedidos_otros_canales").click(
       function (e) {
           busqueda_pedidos_otros_canales()
       }
    )



$(document).ready(function() {
    $("#solicitarCreditoBtn").click(function(event) {

        var aceptaTerminosChecked = $("#acepta_terminos").prop("checked");
        var aceptaCondicionesChecked = $("#acepta_condiciones").prop("checked");

        if (!aceptaTerminosChecked || !aceptaCondicionesChecked) {
            // Si alguno de los checkboxes no está marcado, no proceder con la validación
            alert("Debe aceptar los términos y condiciones antes de continuar.");
            return;
        }
        // Realizar la validación del campo "intereses"
        var intereses = $("#intereses1").val();
        var interesesSinComa = intereses.replace(",", "");

        // Convertir el valor sin coma a un entero
        var intereses = parseInt(interesesSinComa, 10);
        if (intereses < 40001) {
            $("#costoServicio").text(`Señor empresario, el costo de la solicitud del servicio es de ${intereses}, ¿desea continuar?`);
            // Muestra el mensaje de confirmación si los intereses son menores a 40,000
            $("#mensajeConfirmacion").show();
            $("#solicitarCreditoBtn").hide();
        } else {
            // Si los intereses son mayores o iguales a 40,000, envía el formulario
            $("#miFormulario").submit();
        }
    });

    // Manejar el clic en el botón Aceptar
    $("#btnAceptar").click(function() {
        // Realizar las acciones necesarias al aceptar
        console.log("Aceptado");
        // Envía el formulario
        $("#miFormulario").submit();
    });


});




$(document).ready(function() {
    $("#AprobarCreditoBtn").click(function(event) {
        $("#AprobarCreditoBtn").hide();

    });


});



    var busqueda_pedidos_otros_canales_clientes = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/pedidos_otros_canales/informacion_cliente/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&pedido='+pedido+'&estado='+estado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
                                            "<td> Pedido #"+casos[i].num_pedido+"</td>" +
                                            "<td>"+casos[i].fecha+"</td>" +
                                            "<td>"+casos[i].fecha_entrega+"</td>" +
                                            "<td>"+casos[i].hora+"</td>" ;
                                            if (casos[i].estado === 'en proceso') {
                                                lineas += "<td><span class='label label-info'>" + casos[i].estado + "</span></td>";
                                            } else {
                                                lineas += "<td><span class='label label-primary'>" + casos[i].estado + "</span></td>";
                                            }
                                lineas += "<td> <a class='btn btn-info' href='/configuracion/orden_pcs_otroscanales_cliente/detalle/" + casos[i].num_pedido +
    "'><i class='fa fa-mail-forward'></i></a> </td><td> <a class='btn btn-danger' href='/configuracion/orden_pcs_otroscanales_cliente/eliminar/" + casos[i].num_pedido +
    "'><i class='fa fa-mail-forward'></i></a> </td>" +
    "</tr>";

                               }
                        table_body.append(lineas)
    }
    });
    }


    $("#busqueda_pedidos_otros_canales_clientes").click(
       function (e) {
           busqueda_pedidos_otros_canales_clientes()
       }
    )







        //BUSCAR PEDIDOS OTROS CANALES EMPRESARIOS
        var busqueda_pedidos_otros_canales_empresarios = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        empresa_input = $("#empresa_input").val() || "";
        empresa_input = empresa_input.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');
        codigo = $("#codigo").val() || "";
        codigo = codigo.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/pedidos_otros_canales_empresarios/informacion/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa_input='+empresa_input+'&pedido='+pedido+'&estado='+estado+'&codigo='+codigo,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var estado = '';
                        var table_body = $("#tabla_infoc_medicamentos tbody")
                        table_body.empty();
                        for(var i=0;i<casos.length; i++)
                                 {


                                lineas +=   "<tr>" +
            "<td><input type='checkbox' class='pdf-checkbox' value='"+ casos[i].identificador +"'></td>" + // NUEVA CELDA
            "<td> Pedido #"+casos[i].num_pedido+"</td>" +
            "<td>"+casos[i].cliente+"</td>" +
            "<td>"+casos[i].cantidad+"</td>" +
            "<td>"+casos[i].fecha+"</td>" +
            "<td>"+casos[i].referencia+"</td>" +
            "<td>"+casos[i].nombre+"</td>" +
            "<td>"+casos[i].codigo+"</td>" +
            "<td>"+casos[i].empresa+"</td>" +
            "<td>"+casos[i].observaciones+"</td>" +
            "<td> <a class='btn btn-info' href='/configuracion/orden_pcs_otroscanales/detalle/"+ casos[i].num_pedido +
            "'><i class='fa fa-mail-forward'></i></a> </td>" +
            "</tr>";
                               }
                        table_body.append(lineas)
    }
    });
    }


    $("#busqueda_pedidos_otros_canales_empresarios").click(
       function (e) {
           busqueda_pedidos_otros_canales_empresarios()
       }
    )


$('#download-selected-pdfs').on('click', function () {
    var selected = $('.pdf-checkbox:checked');
    if (selected.length === 0) {
        alert("Selecciona al menos un pedido.");
        return;
    }

    var ids = [];
    selected.each(function () {
        ids.push($(this).val());
    });

    fetch('/configuracion/solicitud_asignacion/descargar_zip/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        body: JSON.stringify({ ids: ids })
    })
    .then(function (response) {
        if (!response.ok) throw new Error("Error generando ZIP");
        return response.blob();
    })
    .then(function (blob) {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'pedidos.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    })
    .catch(function (error) {
        console.error("Error:", error);
        alert("Ocurrió un error al generar el archivo ZIP.");
    });
});



var busqueda_pedidos_otros_canales_empresarios_facturar = function () {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var fecha_inicio = $("#fecha_inicio_input").val() || "";
    fecha_inicio = fecha_inicio.replace(/\s+/g, '');
    var fecha_fin = $("#fecha_fin_input").val() || "";
    fecha_fin = fecha_fin.replace(/\s+/g, '');
    var empresa_input = $("#empresa_input").val() || "";
    empresa_input = empresa_input.replace(/\s+/g, '');
    var estado = $("#estado_input").val() || "";
    estado = estado.replace(/\s+/g, '');
    var pedido = $("#pedido").val() || "";
    pedido = pedido.replace(/\s+/g, '');
    var referencia = $("#referencia").val() || "";
    referencia = referencia.replace(/\s+/g, '');
    var u_plu = $("#u_plu").val() || "";
    u_plu = u_plu.replace(/\s+/g, '');

    $.ajax({
        type: "GET",
        data: { csrfmiddlewaretoken: csrfToken },
        url: '/configuracion/pedidos_otros_canales_empresarios/facturar/?fecha_inicio=' + fecha_inicio +
             '&fecha_fin=' + fecha_fin + '&empresa_input=' + empresa_input +
             '&pedido=' + pedido + '&estado=' + estado + '&referencia=' + referencia+'&u_plu=' + u_plu,
        dataType: 'json',
        success: function (data) {
            var casos = data.datos;
            var lineas = '';
            var table_body = $("#tabla_infoc_medicamentos tbody");
            table_body.empty();

            for (var i = 0; i < casos.length; i++) {
                lineas += "<tr>" +
                    "<td>" + casos[i].num_pedido + "</td>" +
                    "<td>" + casos[i].cliente + "</td>" +
                    "<td>" +
                        "<input type='hidden' name='items[" + i + "][pk]' value='" + casos[i].pk + "'>" +
                        "<input type='number' class='form-control' min='0' max='" + casos[i].cantidad +
                        "' name='items[" + i + "][cantidad]' value='" + casos[i].cantidad + "'>" +
                    "</td>" +
                    "<td>" + casos[i].fecha + "</td>" +
                    "<td>" + casos[i].u_plu + "</td>" +
                    "<td>" + casos[i].referencia + "</td>" +
                    "<td>" + casos[i].nombre + "</td>" +
                    "<td>" + casos[i].codigo + "</td>" +
                    "<td>" + casos[i].empresa + "</td>" +
                    "<td>" + casos[i].observaciones + "</td>" +
                "</tr>";
            }

            table_body.append(lineas);
        }
    });
}

$("#busqueda_pedidos_otros_canales_empresarios_facturar").click(function (e) {
    e.preventDefault();
    busqueda_pedidos_otros_canales_empresarios_facturar();
});

$("#form_facturacion").submit(function (e) {
    var pedidos = {};
    $("#tabla_infoc_medicamentos tbody tr").each(function () {
        var pedido = $(this).find("td:first").text().trim();
        pedidos[pedido] = true;
    });

    if (Object.keys(pedidos).length > 1) {
        alert("Solo puedes facturar un pedido a la vez. Filtra por número de pedido antes de enviar.");
        e.preventDefault();
    }
});














var busqueda_pedidos_otros_canales_empresarios_recibo = function () {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    let fecha_inicio = $("#fecha_inicio_input").val() || "";
    fecha_inicio = fecha_inicio.replace(/\s+/g, '');
    let fecha_fin = $("#fecha_fin_input").val() || "";
    fecha_fin = fecha_fin.replace(/\s+/g, '');
    let empresa_input = $("#empresa_input").val() || "";
    empresa_input = empresa_input.replace(/\s+/g, '');
    let estado = $("#estado_input").val() || "";
    estado = estado.replace(/\s+/g, '');
    let pedido = $("#pedido").val() || "";
    pedido = pedido.replace(/\s+/g, '');
    let referencia = $("#referencia").val() || "";
    referencia = referencia.replace(/\s+/g, '');
    let u_plu = $("#u_plu").val() || "";
    u_plu = u_plu.replace(/\s+/g, '');

    $.ajax({
        type: "GET",
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        url: '/configuracion/pedidos_otros_canales_empresarios/recibo/?fecha_inicio=' + fecha_inicio + '&fecha_fin=' + fecha_fin + '&empresa_input=' + empresa_input + '&pedido=' + pedido + '&estado=' + estado + '&referencia=' + referencia +'&u_plu=' + u_plu,
        dataType: 'json',
        success: function (data) {
            const casos = data.datos;
            const table_body = $("#tabla_infoc_medicamentos tbody");
            table_body.empty();
            let lineas = '';

            for (let i = 0; i < casos.length; i++) {
                const idUnico = `novedades_${i}`;
                const formId = `form_${i}`;

                lineas += "<tr>" +
                    // Checkbox para seleccionar
                    "<td><input type='checkbox' class='check-envio' data-id='" + casos[i].pk + "' data-empresa='" + casos[i].empresa + "'></td>" +

                    "<td>Pedido #" + casos[i].num_pedido + "</td>" +
                    "<td>" + casos[i].cliente + "</td>" +

                    // CANTPED (cantidad pedida)
                    "<td>" + (casos[i].cantidad_pedida || casos[i].cantidadped || 0) + "</td>" +

                    "<td>" + casos[i].fecha + "</td>" +
                    "<td>" + casos[i].u_plu + "</td>" +
                    "<td>" + casos[i].referencia + "</td>" +
                    "<td>" + casos[i].nombre + "</td>" +
                    "<td><a href='" + casos[i].imagen + "' target='_blank' class='btn btn-block btn-info'>Ver</a></td>" +
                    "<td>" + casos[i].codigo + "</td>" +
                    "<td>" + casos[i].empresa + "</td>" +

                    // CANTPEN (cantidad pendiente)
                    "<td>" + (casos[i].cantidad_pendiente || casos[i].cantpen || casos[i].cantidad || 0) + "</td>" +

                    // Input de cantidad obligatoria
                    "<td>" +
                        "<input type='number' class='form-control cantidad-input' min='1' " +
                        "max='" + (casos[i].cantidad_pendiente || casos[i].cantidad || 0) + "' " +
                        "name='cantidad' value='" + (casos[i].cantidad_pendiente || casos[i].cantidad || 0) + "'>" +
                    "</td>" +

                    // CANTREC (cantidad recibida)
                    "<td>" + (casos[i].cantidad_recibida || casos[i].cantidadrecibo || 0) + "</td>" +

                    // Novedades
                    "<td>" +
                        "<div class='form-check'>" +
                            "<input class='form-check-input toggle-novedad' type='checkbox' " +
                            "id='" + idUnico + "_check' data-target='" + idUnico + "_textarea'>" +
                            "<label class='form-check-label' for='" + idUnico + "_check'>Agregar</label>" +
                        "</div>" +
                        "<div class='mt-2'>" +
                            "<textarea class='form-control d-none' style='display: none;' " +
                            "name='novedad' id='" + idUnico + "_textarea' rows='2' " +
                            "placeholder='Escribe una novedad...'></textarea>" +
                        "</div>" +
                    "</td>" +

                "</tr>";
            }

            table_body.append(lineas);

            // Mostrar/ocultar textarea según estado del checkbox
            $(".toggle-novedad").change(function () {
                const targetId = $(this).data("target");
                const textarea = $("#" + targetId);
                if (this.checked) {
                    textarea.removeClass("d-none").show();
                } else {
                    textarea.addClass("d-none").hide();
                    textarea.val("");
                }
            });

            // Checkbox seleccionar todos
            $("#select_all").off("change").on("change", function () {
                $(".check-envio").prop("checked", this.checked);
            });

            // Botón para enviar seleccionados (solo se agrega una vez)
            if ($("#enviar_seleccionados").length === 0) {
                $("#tabla_infoc_medicamentos").after(
                    "<div class='col-md-12 mt-3'>" +
                        "<button id='enviar_seleccionados' class='btn btn-success btn-block btn-flat'>" +
                            "<i class='fa fa-envelope'></i> Enviar seleccionados" +
                        "</button>" +
                    "</div>"
                );
            }

            // Enviar seleccionados
            $("#enviar_seleccionados").off("click").on("click", function () {
                const seleccionados = [];

                $(".check-envio:checked").each(function () {
                    const fila = $(this).closest("tr");
                    const cantidad = parseInt(fila.find("input[name='cantidad']").val(), 10);
                    const novedad = fila.find("textarea[name='novedad']").val();

                    if (!cantidad || cantidad <= 0) {
                        alert("Debe ingresar una cantidad válida para todos los pedidos seleccionados.");
                        throw new Error("Cantidad inválida");
                    }

                    seleccionados.push({
                        id: $(this).data("id"),
                        empresa: $(this).data("empresa"),
                        cantidad: cantidad,
                        novedad: novedad || ""
                    });
                });

                if (seleccionados.length === 0) {
                    alert("Debe seleccionar al menos un pedido.");
                    return;
                }

                $.ajax({
                    url: "/configuracion/recibo/otros_canales/",
                    type: "POST",
                    data: JSON.stringify({ pedidos: seleccionados }),
                    dataType: "json",
                    contentType: "application/json",
                    headers: { "X-CSRFToken": csrfToken },
                    success: function (response) {
                        alert("Pedidos enviados correctamente.");
                        busqueda_pedidos_otros_canales_empresarios_recibo();
                    },
                    error: function (xhr) {
                        alert("Error al enviar: " + xhr.responseText);
                    }
                });
            });

            console.log("Datos recibidos:", casos); // Debug opcional
        }
    });
};

$("#busqueda_pedidos_otros_canales_empresarios_recibo").click(function (e) {
    busqueda_pedidos_otros_canales_empresarios_recibo();
});


















var buscar_pedidos_otros_canales_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        empresa_input = $("#empresa_input").val() || "";
        empresa_input = empresa_input.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_pedido_asignaciones_otroscanales/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa_input='+empresa_input+'&pedido='+pedido+'&estado='+estado

    }

    $("#buscar_pedidos_otros_canales_excel_button").click(
       function (e) {
           buscar_pedidos_otros_canales_excel()
       }
    )








var buscar_pedidos_otros_canales_cliente_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_pedido_cliente_otroscanales/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&pedido='+pedido+'&estado='+estado

    }

    $("#buscar_pedidos_otros_canales_cliete_excel_button").click(
       function (e) {
           buscar_pedidos_otros_canales_cliente_excel()
       }
    )






                                             //BUSCAR CONSOLIDADO EN EXCEL

    var buscar_factura_excel = function () {

        solicitud = $("#solicitud_input").val() || "";
        solicitud = solicitud.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_pedido_orden/excel/?solicitud='+solicitud

    }

    $("#buscar_factura_excel_button").click(
       function (e) {
           buscar_factura_excel()
       }
    )




    var buscar_comprobante_excel = function () {

        solicitud = $("#comprobante_dato_excel").val() || "";
        solicitud = solicitud.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_comprobante_egreso/excel/?solicitud='+solicitud

    }

    $("#buscar_comprobante_excel_button").click(
       function (e) {
           buscar_comprobante_excel()
       }
    )




    var buscar_lista_pedido_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_pedido_orden/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado

    }

    $("#buscar_lista_pedido_excel_button").click(
       function (e) {
           buscar_lista_pedido_excel()
       }
    )

    var buscar_edi_otros_canales = function () {

        pedido_pk = $("#pedido_pk").val() || "";
        pedido_pk = pedido_pk.replace(/\s+/g, '');


        window.location.href = '/configuracion/orden_pcs_otroscanales/detalle_edi/?pedido_pk='+pedido_pk

    }

    $("#buscar_edi_otros_canales_button").click(
       function (e) {
           buscar_edi_otros_canales()
       }
    )

    var buscar_historial_email_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/historial_email/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_historial_email_excel_button").click(
       function (e) {
           buscar_historial_email_excel()
       }
    )




    var buscar_historial_email_reenviado = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/historial_email/excel_reenviado/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_historial_email_reenviado_button").click(
       function (e) {
           buscar_historial_email_reenviado()
       }
    )




    var buscar_historial_respuesta_pedido_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/historial_respuesta_pedido/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_historial_respuesta_pedido_excel_button").click(
       function (e) {
           buscar_historial_respuesta_pedido_excel()
       }
    )


    var buscar_historial_correos_enviados_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        email = $("#email").val() || "";
        email = email.replace(/\s+/g, '');
        pedido = $("#pedido").val() || "";
        pedido = pedido.replace(/\s+/g, '');
        const EmpresaSeleccionada = document.getElementById("empresa").value;

        window.location.href = '/configuracion/historial_correos_enviados/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&empresa='+EmpresaSeleccionada+'&email='+email+'&pedido='+pedido

    }

    $("#buscar_historial_correos_enviados_excel_button").click(
       function (e) {
           buscar_historial_correos_enviados_excel()
       }
    )


    var buscar_historial_empresa_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/historial_empresas/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_historial_empresa_excel_button").click(
       function (e) {
           buscar_historial_empresa_excel()
       }
    )



    var buscar_lista_servicio_crediya_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/servicio_crediya/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_lista_servicio_crediya_button").click(
       function (e) {
           buscar_lista_servicio_crediya_excel()
       }
    )


    var buscar_lista_servicio_crediya_excel_informe = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        window.location.href = '/configuracion/servicio_crediya/informe/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado

    }

    $("#buscar_lista_servicio_crediya_informe_button").click(
       function (e) {
           buscar_lista_servicio_crediya_excel_informe()
       }
    )









    var buscar_lista_servicio_credilisto_excel_informe = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        estado = $("#estado_input").val() || "";
        estado = estado.replace(/\s+/g, '');

        window.location.href = '/configuracion/servicio_credilisto/informe/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado

    }

    $("#buscar_lista_servicio_credilisto_informe_button").click(
       function (e) {
           buscar_lista_servicio_credilisto_excel_informe()
       }
    )


    var buscar_lista_servicio_credilisto_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        window.location.href = '/configuracion/servicio_credilisto/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin

    }

    $("#buscar_lista_servicio_credilisto_button").click(
       function (e) {
           buscar_lista_servicio_credilisto_excel()
       }
    )




    var buscar_aviso_recibo_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        orden_compra = $("#orden_compra").val() || "";
        orden_compra = orden_compra.replace(/\s+/g, '');
        factura = $("#factura").val() || "";
        factura = factura.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_aviso_recibo/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&orden_compra='+orden_compra+'&factura='+factura

    }

    $("#buscar_aviso_recibo_excel_button").click(
       function (e) {
           buscar_aviso_recibo_excel()
       }
    )


    var buscar_inventario_excel = function () {

    cliente = $("#cliente_input").val() || "";
    cliente = cliente.replace(/\s+/g, '');
    fecha_fin = $("#selected-date").val() || "";
    fecha_fin = fecha_fin.replace(/\s+/g, '');

    // Verificar si fecha_fin está vacío
    if (fecha_fin === "") {
        alert("Seleccione una fecha de corte"); // Muestra un mensaje de error
        return; // Detener la ejecución de la función
    }

    // Si fecha_fin no está vacío, continuar con la redirección
    window.location.href = '/configuracion/solicitud_inventarios/excel_general/?cliente=' + cliente + '&fecha_fin=' + fecha_fin;
}

    $("#buscar_inventario_excel_button").click(function (e) {
        buscar_inventario_excel();
    });


    var buscar_ventas_excel = function () {

        cliente = $("#cliente_input").val() || "";
        cliente = cliente.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');

        window.location.href = '/configuracion/solicitud_ventas/excel_general/?cliente='+cliente+'&fecha_fin='+fecha_fin+'&fecha_inicio='+fecha_inicio

    }

    $("#buscar_ventas_excel_button").click(
       function (e) {
           buscar_ventas_excel()
       }
    )


    var buscar_estado_cuenta_excel = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');
        codigo_em = $("#codigo_em_input").val() || "";
        codigo_em = codigo_em.replace(/\s+/g, '');
        var isChecked = document.getElementById('check_input').checked;
        if (isChecked){
            check="si";
        }else {
            check="no";
        }


        window.location.href = '/configuracion/solicitud_estado_cuenta/excel_general/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&check='+check+'&form_id='+codigo_em

    }



    $("#buscar_estado_cuenta_excel_button").click(
       function (e) {
           buscar_estado_cuenta_excel()
       }
    )

    //------------------------------------------- REPORTES EN PDF--------------------------------------------------



                                             //BUSCAR CASOS X CEDULA EN PDF

    var buscar_casos_pacientes_cedula_pdf = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_cedula_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/gestion/gentidades/casosxcedula/?paciente_id='+valor_ingresado

    }

    $("#buscar_casos_pacientes_cedula_pdf_button").click(
       function (e) {
           buscar_casos_pacientes_cedula_pdf()
       }
    )

                                            //BUSCAR CASOS X ESTADO EN PDF

    var buscar_casos_pacientes_estado_pdf = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_estado_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/caso_estado_pdf/?estado_id='+valor_ingresado

    }


    $("#buscar_casos_pacientes_estado_pdf_button").click(
       function (e) {
           buscar_casos_pacientes_estado_pdf()
       }
    )


                                            //BUSCAR CASOS X EPS EN PDF

    var buscar_casos_pacientes_eps_pdf = function () {

        valor_ingresado = $("#busqueda_casos_pacientes_eps_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/caso_eps_pdf/?eps_id='+valor_ingresado

    }


    $("#buscar_casos_pacientes_eps_pdf_button").click(
       function (e) {
           buscar_casos_pacientes_eps_pdf()
       }
    )

                                //BUSCAR PACIENTE X CANAL DE INVITACION EN PDF

    var buscar_paciente_canal_invitacion_pdf = function () {

        valor_ingresado = $("#busqueda_pacientes_canal_invitacion_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/paciente_canal_invitacion_pdf/?canal_invitacion='+valor_ingresado

    }


    $("#buscar_pacientes_canal_invitacion_pdf_button").click(
       function (e) {
           buscar_paciente_canal_invitacion_pdf()
       }
    )



                                //BUSCAR PACIENTE X DEPARTAMENTO EN PDF

    var buscar_paciente_departamento_pdf = function () {

        valor_ingresado = $("#busqueda_pacientes_departamento_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/paciente_departamento_pdf/?departamento='+valor_ingresado

    }


    $("#buscar_pacientes_departamento_pdf_button").click(
       function (e) {
           buscar_paciente_departamento_pdf()
       }
    )

                                    //BUSCAR PACIENTE X MUNICIPIO EN PDF

    var buscar_paciente_municipio_pdf = function () {

        valor_ingresado = $("#busqueda_pacientes_municipio_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/paciente_municipio_pdf/?municipio='+valor_ingresado

    }


    $("#buscar_pacientes_municipio_pdf_button").click(
       function (e) {
           buscar_paciente_municipio_pdf()
       }
    )

                                    //BUSCAR PACIENTE X MUNICIPIO EN PDF

    var buscar_paciente_sexo_pdf = function () {

        valor_ingresado = $("#busqueda_pacientes_sexo_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        window.location.href = '/reportes/paciente_sexo_pdf/?sexo='+valor_ingresado

    }


    $("#buscar_pacientes_sexo_pdf_button").click(
       function (e) {
           buscar_paciente_sexo_pdf()
       }
    )

    //_______________________________________________MEDICIONES________________________________________________


    var buscar_indi_casos_estado = function () {

        fecha_inicio = $("#fecha_inicio_input").val() || "";
        fecha_inicio = fecha_inicio.replace(/\s+/g, '');
        fecha_fin = $("#fecha_fin_input").val() || "";
        fecha_fin = fecha_fin.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/configuracion/envio_mail_indicador/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        casos = data.datos;
                        contador = 1;
                        var lineas = '';
                        var table_body = $("#tabla_indicasos_estado tbody");
                        table_body.empty();
                        lineas +=
                        "<div class='row'>"+
                                "<div class='col-md-4 col-sm-6 col-xs-12'>"+
                                  "<div class='info-box'>"+
                                    "<span class='info-box-icon bg-red'><i class='ion ion-ios-people-outline'></i></span>"+
                                    "<div class='info-box-content'>"+
                                      "<a href='/configuracion/historial_correos_no_enviados/?fecha_inicio="+fecha_inicio+"&fecha_fin="+fecha_fin+"'><span class='info-box-text' >"+'CORREOS SIN ENVIAR'+"</span></a>"+
                                      "<span class='info-box-number'>"+data.n_casos_finalizado+"/"+data.total+ "</span>"+
                                      "<strong><i class='fa fa fa-arrow-right'></i>"+data.p_casos_finalizado+"%"+"</strong><br><br>"+
                                    "</div>"+
                                  "</div>"+
                                "</div>"+
                                "<div class='clearfix visible-sm-block'></div>"+

                                "<div class='col-md-4 col-sm-6 col-xs-12'>"+
                                  "<div class='info-box'>"+
                                    "<span class='info-box-icon bg-green'><i class='ion ion-ios-people-outline'></i></span>"+
                                    "<div class='info-box-content'>"+
                                      "<span class='info-box-text'>"+"CORREOS ENVIADOS"+"</span>"+
                                      "<span class='info-box-number'>"+data.n_casos_pendientes+"/"+data.total+"</span>"+
                                      "<strong><i class='fa fa fa-arrow-right'></i>"+data.p_casos_pendientes+"%"+"</strong><br><br>"+
                                    "</div>"+
                                  "</div>"+
                                "</div>"+
                        "<div class='col-md-4 col-sm-6 col-xs-12'>"+
                                  "<div class='info-box'>"+
                                    "<span class='info-box-icon bg-yellow'><i class='ion ion-ios-people-outline'></i></span>"+
                                    "<div class='info-box-content'>"+
                                      "<a href='/configuracion/historial_correos_no_registrados/?fecha_inicio="+fecha_inicio+"&fecha_fin="+fecha_fin+"'><span class='info-box-text'>"+"CORREOS NO PERTENECEN"+"</span></a>"+
                                      "<span class='info-box-number'>"+data.n_casos_no_pertenece+"/"+data.total+"</span>"+
                                      "<strong><i class='fa fa fa-arrow-right'></i>"+data.p_casos_no_pertenece+"%"+"</strong><br><br>"+
                                    "</div>"+
                                  "</div>"+
                                "</div>"+
                          "</div>";

                        var pieChartCanvas = $("#pieChart_casos_estados").get(0).getContext("2d");
                        var pieChart = new Chart(pieChartCanvas);
                        var PieData = [
                          {
                                value: data.p_casos_finalizado,
                                color: "#dd4b39",
                                highlight: "#dd4b39",
                                label: "CORREOS SIN ENVIAR %"
                              },
                              {
                                value:  data.p_casos_pendientes,
                                color: "#50bc37",
                                highlight: "#50bc37",
                                label: "CORREOS ENVIADOS %"
                              },
                            {
                                value:  data.p_casos_no_pertenece,
                                color: "#f5841f",
                                highlight: "#f5841f",
                                label: "CORREOS NO PERTENECE %"
                              }
                        ];
                        var pieOptions = {
                          //Boolean - Whether we should show a stroke on each segment
                          segmentShowStroke: true,
                          //String - The colour of each segment stroke
                          segmentStrokeColor: "#fff",
                          //Number - The width of each segment stroke
                          segmentStrokeWidth: 2,
                          //Number - The percentage of the chart that we cut out of the middle
                          percentageInnerCutout: 50, // This is 0 for Pie charts
                          //Number - Amount of animation steps
                          animationSteps: 100,
                          //String - Animation easing effect
                          animationEasing: "easeOutBounce",
                          //Boolean - Whether we animate the rotation of the Doughnut
                          animateRotate: true,
                          //Boolean - Whether we animate scaling the Doughnut from the centre
                          animateScale: false,
                          //Boolean - whether to make the chart responsive to window resizing
                          responsive: true,
                          // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
                          maintainAspectRatio: true,
                          //String - A legend template
                          legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
                        };
                        //Create pie or douhnut chart
                        // You can switch between pie and douhnut using the method below.
                        pieChart.Doughnut(PieData, pieOptions);
                        table_body.append(lineas)
    }
    });
    }

    $("#buscar_indi_casos_estado_button").click(
       function (e) {
           buscar_indi_casos_estado()
       }
    )

    var buscar_indi_casos_regimen = function () {

            fecha_inicio = $("#fecha_inicio_input").val() || "";
            fecha_inicio = fecha_inicio.replace(/\s+/g, '');
            fecha_fin = $("#fecha_fin_input").val() || "";
            fecha_fin = fecha_fin.replace(/\s+/g, '');
            estado = $("#estado_input").val() || "";
            estado = estado.replace(/\s+/g, '');

            $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/indicadores/caso_regimen/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                    dataType:'json',
                    success: function(data) {
                        // Cargar en tabla
                            casos = data.datos;
                            contador = 1;
                            var lineas = '';
                            var num_regimen = [];
                            var nombre_regimen = [];
                            var table_body = $("#tabla_indicasos_regimen tbody");
                            table_body.empty();
                            for(var i=0;i<casos.length; i++){
                                 nombre_regimen.push(casos[i].regimen__descripcion)
                             }
                            for(var i=0;i<casos.length; i++){
                                 num_regimen.push(casos[i].regimen_count)
                             }

                            var areaChartData = {
                                                      labels: nombre_regimen,
                                                      datasets: [
                                                        {
                                                          label: "EPS",
                                                          fillColor: "rgba(60,141,188,0.9)",
                                                          strokeColor: "rgba(60,141,188,0.8)",
                                                          pointColor: "#84ae40",
                                                          pointStrokeColor: "rgba(60,141,188,1)",
                                                          pointHighlightFill: "#84ae40",
                                                          pointHighlightStroke: "rgba(60,141,188,1)",
                                                          data: num_regimen,
                                                        }
                                                      ]
                                                    };


                            //-------------
                            //- BAR CHART -
                            //-------------
                            var barChartCanvas = $("#barChart").get(0).getContext("2d");
                            var barChart = new Chart(barChartCanvas);
                            var barChartData = areaChartData;
                            var barChartOptions = {
                              //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                              scaleBeginAtZero: true,
                              //Boolean - Whether grid lines are shown across the chart
                              scaleShowGridLines: true,
                              //String - Colour of the grid lines
                              scaleGridLineColor: "rgba(0,0,0,.05)",
                              //Number - Width of the grid lines
                              scaleGridLineWidth: 1,
                              //Boolean - Whether to show horizontal lines (except X axis)
                              scaleShowHorizontalLines: true,
                              //Boolean - Whether to show vertical lines (except Y axis)
                              scaleShowVerticalLines: true,
                              //Boolean - If there is a stroke on each bar
                              barShowStroke: true,
                              //Number - Pixel width of the bar stroke
                              barStrokeWidth: 2,
                              //Number - Spacing between each of the X value sets
                              barValueSpacing: 5,
                              //Number - Spacing between data sets within X values
                              barDatasetSpacing: 1,
                              //Boolean - whether to make the chart responsive
                              responsive: true,
                              maintainAspectRatio: true
                            };

                            barChartOptions.datasetFill = false;
                            barChart.Bar(barChartData, barChartOptions);

                            table_body.append(lineas)

        }
        });
        }

    $("#buscar_indi_casos_regimen_button").click(
       function (e) {
           buscar_indi_casos_regimen()
       }
    )

    var buscar_indi_casos_eps = function () {

            fecha_inicio = $("#fecha_inicio_input").val() || "";
            fecha_inicio = fecha_inicio.replace(/\s+/g, '');
            fecha_fin = $("#fecha_fin_input").val() || "";
            fecha_fin = fecha_fin.replace(/\s+/g, '');
            estado = $("#estado_input").val() || "";
            estado = estado.replace(/\s+/g, '');

            $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/indicadores/caso_eps/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                    dataType:'json',
                    success: function(data) {
                        // Cargar en tabla
                            casos = data.datos;
                            contador = 1;
                            var lineas = '';
                            var num_eps = [];
                            var nombre_eps = [];
                            var table_body = $("#tabla_indicasos_eps tbody");
                            table_body.empty();
                            for(var i=0;i<casos.length; i++){
                                 nombre_eps.push(casos[i].eps__nombre)
                             }
                            for(var i=0;i<casos.length; i++){
                                 num_eps.push(casos[i].eps_count)
                             }

                            var areaChartData = {
                                                      labels: nombre_eps,
                                                      datasets: [
                                                        {
                                                          label: "EPS",
                                                          fillColor: "rgba(60,141,188,0.9)",
                                                          strokeColor: "rgba(60,141,188,0.8)",
                                                          pointColor: "#84ae40",
                                                          pointStrokeColor: "rgba(60,141,188,1)",
                                                          pointHighlightFill: "#84ae40",
                                                          pointHighlightStroke: "rgba(60,141,188,1)",
                                                          data: num_eps,
                                                        }
                                                      ]
                                                    };


                            //-------------
                            //- BAR CHART -
                            //-------------
                            var barChartCanvas = $("#barChart").get(0).getContext("2d");
                            var barChart = new Chart(barChartCanvas);
                            var barChartData = areaChartData;
                            var barChartOptions = {
                              //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                              scaleBeginAtZero: true,
                              //Boolean - Whether grid lines are shown across the chart
                              scaleShowGridLines: true,
                              //String - Colour of the grid lines
                              scaleGridLineColor: "rgba(0,0,0,.05)",
                              //Number - Width of the grid lines
                              scaleGridLineWidth: 1,
                              //Boolean - Whether to show horizontal lines (except X axis)
                              scaleShowHorizontalLines: true,
                              //Boolean - Whether to show vertical lines (except Y axis)
                              scaleShowVerticalLines: true,
                              //Boolean - If there is a stroke on each bar
                              barShowStroke: true,
                              //Number - Pixel width of the bar stroke
                              barStrokeWidth: 2,
                              //Number - Spacing between each of the X value sets
                              barValueSpacing: 5,
                              //Number - Spacing between data sets within X values
                              barDatasetSpacing: 1,
                              //Boolean - whether to make the chart responsive
                              responsive: true,
                              maintainAspectRatio: true
                            };

                            barChartOptions.datasetFill = false;
                            barChart.Bar(barChartData, barChartOptions);

                            table_body.append(lineas)

        }
        });
        }

    $("#buscar_indi_casos_eps_button").click(
       function (e) {
           buscar_indi_casos_eps()
       }
    )

     var buscar_indi_casos_departamentos = function () {

            fecha_inicio = $("#fecha_inicio_input").val() || "";
            fecha_inicio = fecha_inicio.replace(/\s+/g, '');
            fecha_fin = $("#fecha_fin_input").val() || "";
            fecha_fin = fecha_fin.replace(/\s+/g, '');
            estado = $("#estado_input").val() || "";
            estado = estado.replace(/\s+/g, '');

            $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/indicadores/caso_departamentos/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                    dataType:'json',
                    success: function(data) {
                        // Cargar en tabla
                            casos = data.datos;
                            contador = 1;
                            var lineas = '';
                            var num_departamentos = [];
                            var nombre_departamentos = [];
                            var table_body = $("#tabla_indicasos_eps tbody");
                            table_body.empty();

                            for(var i=0;i<casos.length; i++){
                                 nombre_departamentos.push(casos[i].paciente__departamento__nombre)
                             }
                            for(var i=0;i<casos.length; i++){
                                 num_departamentos.push(casos[i].departamentos_count)
                             }

                            var areaChartData = {
                                                      labels: nombre_departamentos,
                                                      datasets: [
                                                        {
                                                          label: "Visitantes",
                                                          fillColor: "rgba(60,141,188,0.9)",
                                                          strokeColor: "rgba(60,141,188,0.8)",
                                                          pointColor: "#84ae40",
                                                          pointStrokeColor: "rgba(60,141,188,1)",
                                                          pointHighlightFill: "#84ae40",
                                                          pointHighlightStroke: "rgba(60,141,188,1)",
                                                          data: num_departamentos
                                                        }
                                                      ]
                                                    };


                            //-------------
                            //- BAR CHART -
                            //-------------
                            var barChartCanvas = $("#barChart").get(0).getContext("2d");
                            var barChart = new Chart(barChartCanvas);
                            var barChartData = areaChartData;
                            var barChartOptions = {
                              //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                              scaleBeginAtZero: true,
                              //Boolean - Whether grid lines are shown across the chart
                              scaleShowGridLines: true,
                              //String - Colour of the grid lines
                              scaleGridLineColor: "rgba(0,0,0,.05)",
                              //Number - Width of the grid lines
                              scaleGridLineWidth: 1,
                              //Boolean - Whether to show horizontal lines (except X axis)
                              scaleShowHorizontalLines: true,
                              //Boolean - Whether to show vertical lines (except Y axis)
                              scaleShowVerticalLines: true,
                              //Boolean - If there is a stroke on each bar
                              barShowStroke: true,
                              //Number - Pixel width of the bar stroke
                              barStrokeWidth: 2,
                              //Number - Spacing between each of the X value sets
                              barValueSpacing: 5,
                              //Number - Spacing between data sets within X values
                              barDatasetSpacing: 1,
                              //Boolean - whether to make the chart responsive
                              responsive: true,
                              maintainAspectRatio: true
                            };

                            barChartOptions.datasetFill = false;
                            barChart.Bar(barChartData, barChartOptions);

                            table_body.append(lineas)

        }
        });
        }

    $("#buscar_indi_casos_departamentos_button").click(
       function (e) {
           buscar_indi_casos_departamentos()
       }
    )


    var buscar_indi_casos_patologias = function () {

            fecha_inicio = $("#fecha_inicio_input").val() || "";
            fecha_inicio = fecha_inicio.replace(/\s+/g, '');
            fecha_fin = $("#fecha_fin_input").val() || "";
            fecha_fin = fecha_fin.replace(/\s+/g, '');
            estado = $("#estado_input").val() || "";
            estado = estado.replace(/\s+/g, '');

            $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/indicadores/caso_patologias/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado,
                    dataType:'json',
                    success: function(data) {
                        // Cargar en tabla
                            casos = data.datos;
                            var num_patologias = [];
                            var nombre_patologias = [];
                            var lineas = '';
                            var table_body = $("#tabla_indicasos_patologias tbody");
                            table_body.empty();

                            for(var i=0;i<casos.length; i++){
                                 nombre_patologias.push(casos[i].enfermedad_establecida__descripcion)
                             }
                            for(var i=0;i<casos.length; i++){
                                 num_patologias.push(casos[i].patologias_count)
                             }

                            var areaChartData = {
                                                      labels: nombre_patologias,
                                                      datasets: [
                                                        {
                                                          label: "Visitantes",
                                                          fillColor: "rgba(60,141,188,0.9)",
                                                          strokeColor: "rgba(60,141,188,0.8)",
                                                          pointColor: "#84ae40",
                                                          pointStrokeColor: "rgba(60,141,188,1)",
                                                          pointHighlightFill: "#84ae40",
                                                          pointHighlightStroke: "rgba(60,141,188,1)",
                                                          data: num_patologias
                                                        }
                                                      ]
                                                    };


                            //-------------
                            //- BAR CHART -
                            //-------------
                            var barChartCanvas = $("#barChart").get(0).getContext("2d");
                            var barChart = new Chart(barChartCanvas);
                            var barChartData = areaChartData;
                            var barChartOptions = {
                              //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                              scaleBeginAtZero: true,
                              //Boolean - Whether grid lines are shown across the chart
                              scaleShowGridLines: true,
                              //String - Colour of the grid lines
                              scaleGridLineColor: "rgba(0,0,0,.05)",
                              //Number - Width of the grid lines
                              scaleGridLineWidth: 1,
                              //Boolean - Whether to show horizontal lines (except X axis)
                              scaleShowHorizontalLines: true,
                              //Boolean - Whether to show vertical lines (except Y axis)
                              scaleShowVerticalLines: true,
                              //Boolean - If there is a stroke on each bar
                              barShowStroke: true,
                              //Number - Pixel width of the bar stroke
                              barStrokeWidth: 2,
                              //Number - Spacing between each of the X value sets
                              barValueSpacing: 5,
                              //Number - Spacing between data sets within X values
                              barDatasetSpacing: 1,
                              //Boolean - whether to make the chart responsive
                              responsive: true,
                              maintainAspectRatio: true
                            };

                            barChartOptions.datasetFill = false;
                            barChart.Bar(barChartData, barChartOptions);

                            table_body.append(lineas)

        }
        });
        }

    $("#buscar_indi_casos_patologias_button").click(
       function (e) {
           buscar_indi_casos_patologias()
       }
    )

    var buscar_indi_pacientes_edad_genero = function () {

            fecha_inicio = $("#fecha_inicio_input").val() || "";
            fecha_inicio = fecha_inicio.replace(/\s+/g, '');
            fecha_fin = $("#fecha_fin_input").val() || "";
            fecha_fin = fecha_fin.replace(/\s+/g, '');
            estado = $("#estado_input").val() || "";
            estado = estado.replace(/\s+/g, '');
            patologia = $("#patologia_input").val() || "";
            patologia = patologia.replace(/\s+/g, '');
            eps = $("#eps_input").val() || "";
            eps = eps.replace(/\s+/g, '');
            departamento = $("#departamento_input").val() || "";
            departamento = departamento.replace(/\s+/g, '');

            $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/indicadores/pacientes_edad_genero/?fecha_inicio='+fecha_inicio+'&fecha_fin='+fecha_fin+'&estado='+estado+'&patologia='+patologia+'&eps='+eps+'&departamento='+departamento,
                    dataType:'json',
                    success: function(data) {
                        // Cargar en tabla
                            hombres = data.hombres;
                            mujeres = data.mujeres;
                            var hcasos = [];
                            var mcasos = [];
                            var lineas = '';
                            var table_body = $("#tabla_indicasos_pacientes_edad_genero tbody");
                            table_body.empty();

                             for(var i=0;i<hombres.length; i++){
                                 hcasos.push(hombres[i].pacientes_count)
                             }

                             for(var i=0;i<mujeres.length; i++){
                                 mcasos.push(mujeres[i].pacientes_count)
                             }

                             lineas +=
                                        "<div class='row'>"+
                                                "<div class='col-md-6 col-sm-6 col-xs-12'>"+
                                                  "<div class='info-box'>"+
                                                    "<span class='info-box-icon bg-blue'><i class='ion ion-ios-people-outline'></i></span>"+
                                                    "<div class='info-box-content'>"+
                                                      "<span class='info-box-text'>"+' TOTAL HOMBRES'+"</span>"+
                                                      "<span class='info-box-number'>"+data.chombre+"</span>"+
                                                    "</div>"+
                                                  "</div>"+
                                                "</div>"+
                                                "<div class='clearfix visible-sm-block'></div>"+
                                                "<div class='col-md-6 col-sm-6 col-xs-12'>"+
                                                  "<div class='info-box'>"+
                                                    "<span class='info-box-icon bg-rosa'><i class='ion ion-ios-people-outline'></i></span>"+
                                                    "<div class='info-box-content'>"+
                                                      "<span class='info-box-text'>"+"TOTAL MUJERES"+"</span>"+
                                                      "<span class='info-box-number'>"+data.cmujer+"</span>"+
                                                    "</div>"+
                                                  "</div>"+
                                                "</div>"+
                                          "</div>";

                            var areaChartData = {
                                  labels: ["1-10 años", "11-20 años", "21-30 años", "31-40 años", "41-50 años",
                                           "51-60 años", "61-70 años", "71-80 años", "81-90 años", "mayor 90 años", ],
                                  datasets: [
                                    {
                                      label: "Mujeres",
                                      fillColor: "rgba(247, 2, 124, 1.0)",
                                      strokeColor: "rgba(247, 2, 124, 1.0)",
                                      pointColor: "rgba(247, 2, 124, 1.0)",
                                      pointStrokeColor: "#ff0080",
                                      pointHighlightFill: "#fff",
                                      pointHighlightStroke: "rgba(220,220,220,1)",
                                      data: mcasos
                                    },
                                    {
                                      label: "Hombres",
                                      fillColor: "rgba(59, 139, 186, 1.0)",
                                      strokeColor: "rgba(59, 139, 186, 1.0)",
                                      pointColor: "#3b8bba",
                                      pointStrokeColor: "rgba(59, 139, 186, 1.0)",
                                      pointHighlightFill: "#fff",
                                      pointHighlightStroke: "rgba(59, 139, 186, 1.0)",
                                      data: hcasos
                                    }
                                  ]
                                };


                            //-------------
                            //- BAR CHART -
                            //-------------
                            var barChartCanvas = $("#barChart").get(0).getContext("2d");
                            var barChart = new Chart(barChartCanvas);
                            var barChartData = areaChartData;
                            barChartData.datasets[1].fillColor = "#3b8bba";
                            barChartData.datasets[1].strokeColor = "#3b8bba";
                            barChartData.datasets[1].pointColor = "#3b8bba";
                            var barChartOptions = {
                              //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                              scaleBeginAtZero: true,
                              //Boolean - Whether grid lines are shown across the chart
                              scaleShowGridLines: true,
                              //String - Colour of the grid lines
                              scaleGridLineColor: "rgba(0,0,0,.05)",
                              //Number - Width of the grid lines
                              scaleGridLineWidth: 1,
                              //Boolean - Whether to show horizontal lines (except X axis)
                              scaleShowHorizontalLines: true,
                              //Boolean - Whether to show vertical lines (except Y axis)
                              scaleShowVerticalLines: true,
                              //Boolean - If there is a stroke on each bar
                              barShowStroke: true,
                              //Number - Pixel width of the bar stroke
                              barStrokeWidth: 2,
                              //Number - Spacing between each of the X value sets
                              barValueSpacing: 5,
                              //Number - Spacing between data sets within X values
                              barDatasetSpacing: 1,
                              //Boolean - whether to make the chart responsive
                              responsive: true,
                              maintainAspectRatio: true
                            };

                            barChartOptions.datasetFill = false;
                            barChart.Bar(barChartData, barChartOptions);

                            table_body.append(lineas)

        }
        });
        }

    $("#buscar_indi_pacientes_edad_genero_button").click(
       function (e) {
           buscar_indi_pacientes_edad_genero()
       }
    )
    //BUSCAR TERCEROS X NOMBRES

    var buscar_terceros_nombre = function () {

        valor_ingresado = $("#busqueda_terceros_nombre_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/r_registrar/?id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        terceros = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_terceros tbody")
                        table_body.empty();
                        for(var i=0;i<terceros.length; i++)
                           {
                            lineas +=

                                "<tr>" +
                                    "<td>"+ terceros[i].id +"</td>" +
                                    "<td>"+ terceros[i].nombre +"</td>" +
                                    "<td>"+ terceros[i].sigla + "</td>" +
                                    "<td>"+ terceros[i].representante_legal + "</td>" +
                                    "<td>"+ terceros[i].telefono + "</td>" +
                                    "<td>"+terceros[i].direccion+"</td>" +
                                    "<td>"+terceros[i].email+"</td>" +

                                "</tr>";

                           }
                        table_body.append(lineas)

    }
    });
    }

    $("#busqueda_123_button").click(
           function (e) {
               buscar_terceros_nombre()
           }
        )


    //BUSCAR TERCEROS X PERSONA

    var buscar_terceros_persona = function () {

        valor_ingresado = $("#busqueda_terceros_persona_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/r_registrar/?id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    // Cargar en tabla
                        terceros = data.datos;
                        var lineas = ''
                        var table_body = $("#tabla_terceros tbody")
                        table_body.empty();
                        for(var i=0;i<terceros.length; i++)
                           {
                            lineas +=

                                "<tr>" +
                                    "<td>"+ terceros[i].id +"</td>" +
                                    "<td>"+ terceros[i].nombre +"</td>" +
                                    "<td>"+ terceros[i].sigla + "</td>" +
                                    "<td>"+ terceros[i].representante_legal + "</td>" +
                                    "<td>"+ terceros[i].telefono + "</td>" +
                                    "<td>"+terceros[i].direccion+"</td>" +
                                    "<td>"+terceros[i].email+"</td>" +

                                "</tr>";

                           }
                        table_body.append(lineas)

    }
    });
    }

    $("#busqueda_persona_button").click(
           function (e) {
               buscar_terceros_persona()
           }
        )




//BUSCAR DATOS EMPRESA PARA EDITAR
    var editar_terceros_nombre = function () {

        valor_ingresado = $("#busqueda_terceros_nombre_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/r_registrar/?id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    terceros = data.datos;
                    for(var i=0;i<terceros.length; i++)
                           {
                               document.getElementById('nombre_editar').value=terceros[i].nombre
                               document.getElementById('id_editar').value=terceros[i].id
                               document.getElementById('nit_editar').value=terceros[i].nit
                               document.getElementById('dv_editar').value=terceros[i].dv
                               document.getElementById('sigla_editar').value=terceros[i].sigla
                               document.getElementById('direccion_editar').value=terceros[i].direccion
                               document.getElementById('telefono_editar').value=terceros[i].telefono
                               document.getElementById('telefono2_editar').value=terceros[i].telefono2
                               document.getElementById('celular_editar').value=terceros[i].celular
                               document.getElementById('email_editar').value=terceros[i].email
                               document.getElementById('representante_legal_editar').value=terceros[i].representante_legal
                               document.getElementById('paises').options[document.getElementById('paises').selectedIndex].text=terceros[i].paises_nombre;
                               document.getElementById('paises').options[document.getElementById('paises').selectedIndex].value=terceros[i].paises;
                               document.getElementById('continentes').options[document.getElementById('continentes').selectedIndex].text=terceros[i].continentes_nombre;
                               document.getElementById('continentes').options[document.getElementById('continentes').selectedIndex].value=terceros[i].continentes;
                               document.getElementById('departamentos').options[document.getElementById('departamentos').selectedIndex].text=terceros[i].departamentos_nombre;
                               document.getElementById('departamentos').options[document.getElementById('departamentos').selectedIndex].value=terceros[i].departamentos;
                               document.getElementById('municipios').options[document.getElementById('municipios').selectedIndex].text=terceros[i].municipios_nombre;
                               document.getElementById('municipios').options[document.getElementById('municipios').selectedIndex].value=terceros[i].municipios;
                               document.getElementById('tipo_tercero').options[document.getElementById('tipo_tercero').selectedIndex].text=terceros[i].tipo_tercero_nombre;
                               document.getElementById('tipo_tercero').options[document.getElementById('tipo_tercero').selectedIndex].value=terceros[i].tipo_tercero;
                           }
    }
    });
    }

    $("#busqueda_editar_button").click(
           function (e) {
               editar_terceros_nombre()
           }
        )

//BUSCAR DATOS PERSONA PARA EDITAR
    var editar_terceros_persona = function () {

        valor_ingresado = $("#busqueda_terceros_persona_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/r_registrar/?id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    terceros = data.datos;
                    for(var i=0;i<terceros.length; i++)
                           {
                               document.getElementById('nombre_editar').value=terceros[i].nombre
                               document.getElementById('id_editar').value=terceros[i].id
                               document.getElementById('nit_editar').value=terceros[i].nit
                               document.getElementById('dv_editar').value=terceros[i].dv
                               document.getElementById('sigla_editar').value=terceros[i].sigla
                               document.getElementById('direccion_editar').value=terceros[i].direccion
                               document.getElementById('telefono_editar').value=terceros[i].telefono
                               document.getElementById('telefono2_editar').value=terceros[i].telefono2
                               document.getElementById('celular_editar').value=terceros[i].celular
                               document.getElementById('email_editar').value=terceros[i].email
                               document.getElementById('representante_legal_editar').value=terceros[i].representante_legal
                               document.getElementById('paises').options[document.getElementById('paises').selectedIndex].text=terceros[i].paises_nombre;
                               document.getElementById('paises').options[document.getElementById('paises').selectedIndex].value=terceros[i].paises;
                               document.getElementById('continentes').options[document.getElementById('continentes').selectedIndex].text=terceros[i].continentes_nombre;
                               document.getElementById('continentes').options[document.getElementById('continentes').selectedIndex].value=terceros[i].continentes;
                               document.getElementById('departamentos').options[document.getElementById('departamentos').selectedIndex].text=terceros[i].departamentos_nombre;
                               document.getElementById('departamentos').options[document.getElementById('departamentos').selectedIndex].value=terceros[i].departamentos;
                               document.getElementById('municipios').options[document.getElementById('municipios').selectedIndex].text=terceros[i].municipios_nombre;
                               document.getElementById('municipios').options[document.getElementById('municipios').selectedIndex].value=terceros[i].municipios;
                               document.getElementById('tipo_tercero').options[document.getElementById('tipo_tercero').selectedIndex].text=terceros[i].tipo_tercero_nombre;
                               document.getElementById('tipo_tercero').options[document.getElementById('tipo_tercero').selectedIndex].value=terceros[i].tipo_tercero;
                           }
    }
    });
    }

    $("#busqueda_editar_button_persona").click(
           function (e) {
               editar_terceros_persona()
           }
        )






//BUSCAR SUBEXPEDIENTE PARA EDITAR
    var editar_sub_expedientes = function () {

        valor_ingresado = $("#sub_expediente_data_input").val() || ""
        valor_ingresado = valor_ingresado.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/sub_expedientes/r_listar/?id='+valor_ingresado,
                dataType:'json',
                success: function(data) {
                    subexpedientes = data.datos;
                    for(var i=0;i<subexpedientes.length; i++)
                           {
                               document.getElementById('nombre_subexpediente').value=subexpedientes[i].nombre
                               document.getElementById('numero_carpeta_subexpediente').value=subexpedientes[i].numero_carpeta
                               document.getElementById('numero_folios_subexpedientes').value=subexpedientes[i].numero_folios

                           }
    }
    });
    }

    $("#sub_expediente_data_input").click(
           function (e) {
               editar_sub_expedientes()
           }
        )




    var buscar_agenda = function () {

            fecha = $("#fecha").val() || "";
            fecha = fecha.replace(/\s+/g, '');
            responsable = $("#responsable").val() || "";
            responsable = responsable.replace(/\s+/g, '');
            $("#calendario_agenda_trabajo").fullCalendar('destroy');

             $.ajax({
                    type: "GET",
                    data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    url: '/gestion/ragenda/?fecha='+fecha+'&responsable='+responsable,
                    dataType:'json',
                    success: function(data) {
                            agenda = data.datos;
                            var lista_agenda = [];
                                function ini_events(ele) {
                                  ele.each(function () {

                                    var eventObject = {
                                      title: $.trim($(this).text()) // use the element's text as the event title
                                    };

                                    $(this).data('eventObject', eventObject);

                                    $(this).draggable({
                                      zIndex: 1070,
                                      revert: true, // will cause the event to go back to its
                                      revertDuration: 0  //  original position after the drag
                                    });

                                  });
                                }

                                ini_events($('#external-events div.external-event'));
                            /* initialize the calendar
                                 -----------------------------------------------------------------*/
                                //Date for the calendar events (dummy data)


                            for(var i=0;i<agenda.length; i++){
                                     var color = agenda[i].color
                                     var date = new Date(agenda[i].fecha)
                                     var h = agenda[i].h
                                     var min = agenda[i].m
                                     var d = agenda[i].dia
                                     m = date.getMonth()
                                     y = date.getFullYear()

                                     if (agenda[i].tiempo === 1) {
                                     var tiempo = true
                                     }else {
                                     var tiempo = false
                                     }

                                     lista_agenda.push(
                                       {
                                       title: agenda[i].paciente ,
                                       start: new Date(y, m, d, h, min),
                                       allDay: tiempo,
                                       url: '/administracion/gestion/agenda/?id='+agenda[i].id,
                                       backgroundColor: color,
                                       borderColor: color
                                      }
                                    );
                                }

                                $('#calendario_agenda_trabajo').fullCalendar({
                                  viewRender: function(currentView){
                                        var minDate = new Date(fecha);
                                        var maxDate = new Date(fecha);
                                        maxDate.setMonth(maxDate.getMonth() + 1);
                                        // Past
                                        if (minDate >= currentView.start && minDate <= currentView.end) {
                                            $(".fc-prev-button").prop('disabled', true);
                                            $(".fc-prev-button").addClass('fc-state-disabled');
                                        }
                                        else {
                                            $(".fc-prev-button").removeClass('fc-state-disabled');
                                            $(".fc-prev-button").prop('disabled', false);
                                        }
                                        // Future
                                        if (maxDate >= currentView.start && maxDate <= currentView.end) {
                                            $(".fc-next-button").prop('disabled', true);
                                            $(".fc-next-button").addClass('fc-state-disabled');
                                        } else {
                                            $(".fc-next-button").removeClass('fc-state-disabled');
                                            $(".fc-next-button").prop('disabled', false);
                                        }
                                    },
                                  defaultDate: fecha,
                                  monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
                                  monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
                                  dayNames: ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'],
                                  dayNamesShort: ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'],
                                  defaultButtonText: {
                                        prev: "prev",
                                        next: "next",
                                        prevWeek: "prevWeek",
                                        nextWeek: "nextWeek",
                                        prevYear: "prev year",
                                        nextYear: "next year",
                                        today: 'Hoy',
                                        month: 'Mes',
                                        week: 'Semana',
                                        day: 'Día'
                                    },

                                  header: {
                                    left: 'prev,next',
                                    center: 'title',
                                    right: 'month,agendaWeek,agendaDay'
                                  },
                                  events :  lista_agenda
                                });





        }
        });
        }

    $("#buscar_agenda_button").click(
       function (e) {
           buscar_agenda()
       }
    )

     // CALENDARIO AGENDA DE TRABAJO

mobiscroll.setOptions({
    locale: mobiscroll.localeEs,
    theme: 'ios',
    themeVariant: 'light'
});



     // CALENDARIO AGENDA DE TRABAJO (carga automatica)




})

                                // ACTUALIZAR MEDICOS SEGUN ENTIDAD

    function actualizar_medicos(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('medico');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                entidad: value
            },
            url: '/gestion/gentidades/contactos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                contactos_entidad = data.datos;

                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < contactos_entidad.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = contactos_entidad[i].id_contacto;
                    opt.innerHTML = contactos_entidad[i].nombre_completo;
                    select.appendChild(opt);
                }
            }
        });

    }


                            // ACTUALIZAR CASOS SEGUN ENTIDAD

    function actualizar_casos(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('medico');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                entidad: value
            },
            url: '/gestion/gentidades/contactos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                contactos_entidad = data.datos;

                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < contactos_entidad.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = contactos_entidad[i].id_contacto;
                    opt.innerHTML = contactos_entidad[i].nombre_completo;
                    select.appendChild(opt);
                }
            }
        });

    }

    function validarNumeros(e)
        {
        var keynum = window.event ? window.event.keyCode : e.which;
        if ((keynum == 8) || (keynum == 46))
        return true;

        return /\d/.test(String.fromCharCode(keynum));
        }

function activar(elemento)
                                {
                                    if(elemento.estado.options[elemento.estado.selectedIndex].value=="2")
                                      {document.getElementById("aparece").style.display = "inline";}
                                    else
                                      {document.getElementById("aparece").style.display = "none";}
                                }
function activar2(elemento)
                                {
                                    if(elemento.mayor_edad.options[elemento.mayor_edad.selectedIndex].value=="2")
                                      {document.getElementById("parentesco").style.display = "inline";
                                      document.getElementById("identificacion_familiar").style.display = "inline";
                                      document.getElementById("nombre_uno_familiar").style.display = "inline";
                                      document.getElementById("nombre_dos_familiar").style.display = "inline";
                                      document.getElementById("apellido_uno_familiar").style.display = "inline";
                                      document.getElementById("apellido_dos_familiar").style.display = "inline";
                                      document.getElementById("telefono_familiar").style.display = "inline";
                                      document.getElementById("direccion_residencia_familiar").style.display = "inline";
                                      document.getElementById("codigo_pais_familiar").style.display = "inline";
                                      document.getElementById("codigo_departamento_familiar").style.display = "inline";
                                      document.getElementById("codigo_municipio_familiar").style.display = "inline";}
                                    else
                                      {document.getElementById("parentesco").style.display = "none";
                                      document.getElementById("identificacion_familiar").style.display = "none";
                                      document.getElementById("nombre_uno_familiar").style.display = "none";
                                      document.getElementById("nombre_dos_familiar").style.display = "none";
                                      document.getElementById("apellido_uno_familiar").style.display = "none";
                                      document.getElementById("apellido_dos_familiar").style.display = "none";
                                      document.getElementById("telefono_familiar").style.display = "none";
                                      document.getElementById("direccion_residencia_familiar").style.display = "none";
                                      document.getElementById("codigo_pais_familiar").style.display = "none";
                                      document.getElementById("codigo_departamento_familiar").style.display = "none";
                                      document.getElementById("codigo_municipio_familiar").style.display = "none";}
                                }

function abrir(url)             {
                                    open(url,'','top=300,left=300,width=300,height=300') ;
                                }



// VENTANA EMERGENTE

function popitup(url)           {
                                    newwindow=window.open(url,'{{title}}','height=500,width=800');
                                    if (window.focus) {newwindow.focus()}
                                    return false;
                                }

//FUNCIONES PARA HABILITAR O DESHABILITAR CAMPOS EMEMERGENTES DE UN CAMPO DEL FORMULARIO

function a_enfermedad(elemento) {
                                if (elemento.enfermedad.options[elemento.enfermedad.selectedIndex].value == "1") {
                                    document.getElementById("a_otra_enfermedad").style.display = "inline";
                                }
                                else {
                                    document.getElementById("a_otra_enfermedad").style.display = "none";
                                }
                            }

function a_barrera(elemento) {
                                if (elemento.barrera.options[elemento.barrera.selectedIndex].value == "1") {
                                    document.getElementById("a_otra_barrera").style.display = "inline";
                                }
                                else {
                                    document.getElementById("a_otra_barrera").style.display = "none";
                                }
                            }

function a_encuesta(elemento) {
                                if (elemento.encuesta.options[elemento.encuesta.selectedIndex].value == "SI") {
                                    document.getElementById("active_encuesta").style.display = "inline";
                                }
                                else {
                                    document.getElementById("active_encuesta").style.display = "none";
                                }
                            }

function a_hora(elemento) {
                                if (elemento.tiempo.options[elemento.tiempo.selectedIndex].value == "2") {
                                    document.getElementById("active_hora").style.display = "inline";
                                }
                                else {
                                    document.getElementById("active_hora").style.display = "none";
                                }
                            }

function a_estado_barrera(elemento) {
                               if (elemento.estado_barrera.options[elemento.estado_barrera.selectedIndex].value == "5") {
                                     $('#fecha_formula_medica').prop("required", true);
                                     $('#fecha_entrega_aplicacion').prop("required", true);
                                }
                            }


function a_color(elemento) {
                                if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "1") {
                                    document.getElementById("active_color").style.background= "#00c0ef";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "2") {
                                    document.getElementById("active_color").style.background = "#FF110A";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "3") {
                                    document.getElementById("active_color").style.background = "#59DB1A";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "4") {
                                    document.getElementById("active_color").style.background = "#8EF56B";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "5") {
                                    document.getElementById("active_color").style.background = "#f39c12";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "12") {
                                    document.getElementById("active_color").style.background = "#CD00FF";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "13") {
                                    document.getElementById("active_color").style.background = "#F526B0";
                                }
                                else if (elemento.responsable.options[elemento.responsable.selectedIndex].value == "14") {
                                    document.getElementById("active_color").style.background = "#00a65a";
                                }
                                else {
                                    document.getElementById("active_color").style.background = "#3c8dbc";
                                }
                            }

function printDiv(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;

}

function VerEmpresas() {
        element = document.getElementById("formulario");
        check = document.getElementById("check");
        check_persona=document.getElementById("check_personas")
        var pagare = document.getElementById('pagare_formato');
        var contrato = document.getElementById('contrato_formato');
        var carta = document.getElementById('carta_formato');
        var ficha = document.getElementById('ficha_formato');
        if (check.checked) {
            check_persona.style.display='none';
            element.style.display='block';
            pagare.href = '/bodega/PAGAREPERSONANATURALNUEVO.pdf';
            contrato.href = '/bodega/CONTRATOCREDITONUEVO.pdf';
            carta.href = '/bodega/CARTADEINSTRUCCIONESPERSONANATURALNUEVO.pdf';
            ficha.href = '/bodega/FichaNegociacion.pdf';
        }
        else {
            check_persona.style.display='block';
            element.style.display='none';
        }
    }


function VerPersonas() {
        element = document.getElementById("formulario");
        check = document.getElementById("check_personas");
        check_empresa=document.getElementById("check")
        var pagare = document.getElementById('pagare_formato');
        var contrato = document.getElementById('contrato_formato');
        var carta = document.getElementById('carta_formato');
        var ficha = document.getElementById('ficha_formato');
        if (check.checked) {
            check_empresa.style.display='none'
            element.style.display='block';
            pagare.href = '/bodega/PAGAREPERSONAJURIDICANUEVO.pdf';
            contrato.href = '/bodega/CONTRATOCREDITONUEVO.pdf';
            carta.href = '/bodega/CARTADEINSTRUCCIONESPERSONAJURIDICANUEVO.pdf';
            ficha.href = '/bodega/FichaNegociacion.pdf';
        }
        else {
            check_empresa.style.display='block';
            element.style.display='none';
        }
    }

function VerTerceros() {
        element = document.getElementById("content");
        terceros = document.getElementById("terceros");
        remitente=document.getElementById("remitente")
        if (terceros.checked) {
            remitente.style.display='none';
            element.style.display='block';
        }
        else {
            remitente.style.display='block';
            element.style.display='none';
        }
    }

function VerRemitente() {
        terceros = document.getElementById("terceros");
        remitente=document.getElementById("remitente")
        if (remitente.checked) {
            terceros.style.display='none';
        }
        else {
            terceros.style.display='block';
        }
    }

function cargarCampos(){
 VerEmpresas();
 VerPersonas();

}

//------------------------------------- FUNCIONES GESTION DOCUMENTAL ---------------------------------------

function obtener_id_trd(selectObject) {

        series = $("#series_mostrar").val() || "";
        series = series.replace(/\s+/g, '');
        subseries = $("#subseries_mostrar").val() || "";
        subseries = subseries.replace(/\s+/g, '');
        tipo_documento = $("#tipo_documento_mostrar").val() || "";
        tipo_documento = tipo_documento.replace(/\s+/g, '');
        dependencias = $("#dependencias").val() || "";
        dependencias = dependencias.replace(/\s+/g, '');

        $.ajax({
                type: "GET",
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                url: '/radicados/radicar/expedientes/numero/?dependencias='+dependencias+'&series='+series+'&subseries='+subseries+'&tipo_documento='+tipo_documento,
                dataType:'json',
                success: function(data) {
                    trd = data.datos;
                    for(var i=0;i<trd.length; i++)
                           {
                               document.getElementById('numero_serie').value=trd[i].id

                           }
    }
    });
    }

    // Funcion Paises
function obtener_paises(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('paises');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/paises/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                paises = data.datos;
                var pais_valores=$(paises).filter(function (i,n){return n.continentes===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < pais_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = pais_valores[i].id;
                    opt.innerHTML = pais_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }

// Funcion Departamentos
function obtener_departamentos(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('departamentos');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/departamentos/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                departamentos = data.datos;
                var departamento_valores=$(departamentos).filter(function (i,n){return n.paises===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < departamento_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = departamento_valores[i].id;
                    opt.innerHTML = departamento_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }


// Funcion Municipios
function obtener_municipios(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('municipios');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/municipios/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                municipios = data.datos;
                var municipio_valores=$(municipios).filter(function (i,n){return n.departamentos===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < municipio_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = municipio_valores[i].id;
                    opt.innerHTML = municipio_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }


// Funcion seleccion campos
function a_tipos_radicados(elemento) {
                                if (elemento.tipos_radicados.options[elemento.tipos_radicados.selectedIndex].value == "1") {
                                    document.getElementById("a_medios_recepcion").style.display = "inline";
                                    document.getElementById("a_tipos_envios").style.display = "none";

                                }

                                else if (elemento.tipos_radicados.options[elemento.tipos_radicados.selectedIndex].value == "2") {
                                    document.getElementById("a_medios_recepcion").style.display = "none";
                                    document.getElementById("a_tipos_envios").style.display = "inline";

                                }

                                else {
                                    document.getElementById("a_medios_recepcion").style.display = "none";
                                    document.getElementById("a_tipos_envios").style.display = "none";
                                }
                            }

//SELECCION FUNCIONARIO POR DEPENDENCIA
function obtener_funcionarios(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('funcionario_destino');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/radicados/radicar/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                funcionario_destino = data.datos;
                var funcionarios_valores=$(funcionario_destino).filter(function (i,n){return n.dependencias===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < funcionarios_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = funcionarios_valores[i].id;
                    opt.innerHTML = funcionarios_valores[i].persona_nombre;
                    select.appendChild(opt);
                }
            }
        });

    }

//SELECCION USUARIOS POR DEPENDENCIA
function obtener_usuarios(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('usuario_destino');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/radicados/radicar/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                funcionario_destino = data.datos;
                var funcionarios_valores=$(funcionario_destino).filter(function (i,n){return n.dependencias===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < funcionarios_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = funcionarios_valores[i].id;
                    opt.innerHTML = funcionarios_valores[i].persona_nombre;
                    select.appendChild(opt);
                }
            }
        });

    }


//SELECCION USUARIOS POR DEPENDENCIA CHECK MULTIPLE
function obtener_usuarios_multiple(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('usuario_destino');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/radicados/radicar/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                funcionario_destino = data.datos;
                var funcionarios_valores=$(funcionario_destino).filter(function (i,n){return n.dependencias===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < funcionarios_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = funcionarios_valores[i].id;
                    opt.innerHTML = funcionarios_valores[i].persona_nombre;
                    select.appendChild(opt);
                }
            }
        });

    }



//OBTENER SERIE POR SUBSERIE
function obtener_subseries(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('subseries');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/trd/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                subseries = data.datos;
                var subseries_valores=$(subseries).filter(function (i,n){return n.series===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < subseries_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = subseries_valores[i].id;
                    opt.innerHTML = subseries_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }



//OBTENER SERIE POR SUBSERIE NUMERO
function obtener_subseries_numero(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('subseries_mostrar');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/trd/datos/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                subseries = data.datos;
                var subseries_valores=$(subseries).filter(function (i,n){return n.series===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < subseries_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = subseries_valores[i].id;
                    opt.innerHTML = subseries_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }



//OBTENER EMPRESAS POR TIPO
function obtener_empresa_codigo(selectObject) {
        var value = selectObject.value;
        var codigo = value.split('-')[0];
        $("#codigoempresa").text(codigo);

    }




function obtener_empresa_tipo(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('empresa_usuario');
        tipo_empresa = $("#tipo_empresa").val() || "";
        tipo_empresa = tipo_empresa.replace(/\s+/g, '');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/consultar/empresas_codigos/datos/?tipo_empresa='+tipo_empresa,
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                trd = data.datos;
                var trd_valores=$(trd).filter(function (i,n){return n.tipo_empresa===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < trd_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = trd_valores[i].codigo;
                    opt.innerHTML = trd_valores[i].nombre;
                    select.appendChild(opt);
                }
            }
        });

    }




function obtener_dependencias_subseries_numero(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('tipo_documento_mostrar');
        dependencias = $("#dependencias").val() || "";
        dependencias = dependencias.replace(/\s+/g, '');
        series = $("#series_mostrar").val() || "";
        series = series.replace(/\s+/g, '');
        subseries = $("#subseries_mostrar").val() || "";
        subseries = subseries.replace(/\s+/g, '');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/configuracion/trd/dependencia/datos/?dependencias='+dependencias+'&series='+series+'&subseries='+subseries,
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                trd = data.datos;
                var trd_valores=$(trd).filter(function (i,n){return n.subseries===value});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < trd_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = trd_valores[i].id;
                    opt.innerHTML = trd_valores[i].descripcion;
                    select.appendChild(opt);
                }
            }
        });

    }


    //OBTENER SUBEXPEDIENTES POR EXPEDIENTE
function obtener_subexpediente_ex(selectObject) {
        var value = selectObject.value;
        var select = document.getElementById('subexpediente');

        $.ajax({
            type: "GET",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,

            },
            url: '/radicados/radicar/sub_expedientes/listar/',
            dataType: 'json',
            success: function (data) {
                // Cargar en Select
                subexpediente = data.datos;
                var subexpediente_valores=$(subexpediente).filter(function (i,n){return n.expediente===value || n.expediente==='NS'});


                select.options.length = 0;

                var opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = '';
                opt.selected = true;
                opt.disabled = true;
                select.appendChild(opt);

                for (var i = 0; i < subexpediente_valores.length; i++) {
                    var opt = document.createElement('option');
                    opt.value = subexpediente_valores[i].id;
                    opt.innerHTML = subexpediente_valores[i].nombre;
                    select.appendChild(opt);
                }
            }
        });

    }



    //CREAR EXCEL DE INFORME DE TRD
var tableToExcel = (function() {
  var uri = 'data:application/vnd.ms-excel;base64,'
    , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
    , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
    , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
  return function(table, name) {
    if (!table.nodeType) table = document.getElementById(table)
    var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
    var link = document.createElement("a");
        link.download = "InformeTRD";
        link.href = uri + base64(format(template, ctx))
        link.click();
  }
})()



$("#direcciondependencia").keyup(function(){
        var ta      =   $("#descripciondependencia");
        letras      =   ta.val().trim();
        ta.val(letras)
});