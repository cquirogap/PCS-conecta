# -*- coding: utf-8 -*-
from django import forms


class DatosAdicionales(forms.Form):
    CSS_SELECT2 = 'form-control select2'
    CSS_STYLE_WIDTH = 'width: 100%;'
    FORM_CLASS = 'form-control'
    AREA_RURAL = 'Area Rural'
    AREA_URBANA = 'Area Urbana'
    UBICACIONES = (
        ('No aplica', u'No aplica'),
        (AREA_RURAL, 'Area Rural'),
        (AREA_URBANA, 'Area Urbana')
    )
    TIEMPO_SIN_MEDICACION = (
        ('No aplica', u'No aplica'),
        ('1-5 días', u'De 1 a 5 días'),
        ('6-10 días', u'De 6 a 10 días'),
        ('11-15 días', u'De 11 a 15 días'),
        ('15-30 días', u'16 a 30 días'),
        ('Más de un mes', u'Más de un mes')
    )
    DEMORAS = (
        ('No aplica', u'No aplica'),
        ('Agenda', 'No hay agenda'),
        ('Convenio', 'No hay convenio con la EPS'),
        ('Cartera', 'No se ha pagado la cartera morosa')
    )

    ubicacion = forms.ChoiceField(
        choices=UBICACIONES,
        label=u'Ubicación geográfica'

    )

    medicacion = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label='¿Cuanto tiempo lleva sin tomar el medicamento?'
    )

    ultima_fecha_consulta = forms.DateField(
        required=False,
        input_formats=('%m/%d/%Y'),
        label=u'Última fecha de consulta con médico general o especialista'
    )

    cambio_medicamento = forms.CharField(
        required=False,
        label='¿Le cambiaron el medicamento?'
    )

    cambio_sintomas = forms.CharField(
        required=False,
        label='Ha presentado algo diferente desde que lo cambiaron'
    )

    ubicacion.widget.attrs['class'] = CSS_SELECT2
    ubicacion.widget.attrs['style'] = CSS_STYLE_WIDTH

    medicacion.widget.attrs['class'] = CSS_SELECT2
    medicacion.widget.attrs['style'] = CSS_STYLE_WIDTH

    ultima_fecha_consulta.widget.attrs['class'] = FORM_CLASS
    cambio_medicamento.widget.attrs['class'] = FORM_CLASS
    cambio_sintomas.widget.attrs['class'] = FORM_CLASS

    # Campos de 'barreras de acceso'
    cita_general = forms.ChoiceField(
        choices=(
            ('No aplica', u'No aplica'),
            ('Agenda', 'No hay agenda'),
            ('Convenio', 'No hay convenio EPS')
        ),
        label='Cita con médico general'
    )

    cita_especialista = forms.CharField(
        required=False,
        label='Cita con médico especialista y cuál especialidad'
    )

    especialidad_medico = forms.ChoiceField(
        choices=(('No aplica', u'No aplica'),('General', 'General'), ('Especialista', 'Especialista')),
        label=u'Especialidad Médico'
    )

    demora_autorizacion = forms.ChoiceField(
        choices=DEMORAS,
        label=u'Demora en las Autorización para exámenes clínicos'
    )

    demora_pos = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label=u'Demora en las Autorización de medicamentos POS'
    )

    demora_no_pos = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label=u'Demora en las Autorización de medicamentos NO POS.'
    )

    demora_examenes = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label=u'Demora en la toma de exámenes clínicos'
    )

    demora_medicamentos_pos = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label='Demora en la entrega de medicamentos POS'
    )

    demora_medicamentos_no_pos = forms.ChoiceField(
        choices=TIEMPO_SIN_MEDICACION,
        label='Demora en la entrega de medicamentos NO POS'
    )

    formato_vigilancia = forms.CharField(
        required=False,
        label='Le Solicitan formatos de Farmacovigilancia'
    )

    presenta_tutela = forms.ChoiceField(
        choices=(('No', 'No'), ('Si', 'Si')),
        label='¿Presenta tutela?'
    )

    tipo_tutela = forms.ChoiceField(
        choices=(('No selecciono tipo', u'Seleccione el tipo'),('Integral', u'Integral'), ('Especifica', u'Específica')),
        label=u'Si presenta tutela, ¿de qué tipo es la tutela?'
    )

    cita_general.widget.attrs['class'] = CSS_SELECT2
    cita_general.widget.attrs['style'] = CSS_STYLE_WIDTH

    cita_especialista.widget.attrs['class'] = FORM_CLASS

    especialidad_medico.widget.attrs['class'] = CSS_SELECT2
    especialidad_medico.widget.attrs['style'] = CSS_STYLE_WIDTH

    formato_vigilancia.widget.attrs['class'] = FORM_CLASS

    demora_autorizacion.widget.attrs['class'] = CSS_SELECT2
    demora_autorizacion.widget.attrs['style'] = CSS_STYLE_WIDTH

    demora_pos.widget.attrs['class'] = CSS_SELECT2
    demora_pos.widget.attrs['style'] = CSS_STYLE_WIDTH

    demora_no_pos.widget.attrs['class'] = CSS_SELECT2
    demora_no_pos.widget.attrs['style'] = CSS_STYLE_WIDTH

    demora_examenes.widget.attrs['class'] = CSS_SELECT2
    demora_examenes.widget.attrs['style'] = CSS_STYLE_WIDTH

    demora_medicamentos_pos.widget.attrs['class'] = CSS_SELECT2
    demora_medicamentos_pos.widget.attrs['style'] = CSS_STYLE_WIDTH

    demora_medicamentos_no_pos.widget.attrs['class'] = CSS_SELECT2
    demora_medicamentos_no_pos.widget.attrs['style'] = CSS_STYLE_WIDTH

    presenta_tutela.widget.attrs['style'] = CSS_STYLE_WIDTH

    tipo_tutela.widget.attrs['style'] = CSS_STYLE_WIDTH
