# -*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import LoginAttemptDjango


class CustomAuthenticationForm(AuthenticationForm):
    max_failed_attempts = 5
    lockout_duration = timedelta(minutes=5)
    invalid_credentials = _(u"No pudimos iniciar sesión. Revisa tus datos o inténtalo más tarde.")
    error_messages = {
        'invalid_login': invalid_credentials,
        'inactive': invalid_credentials,
    }

    def _invalid_login_error(self):
        return forms.ValidationError(self.invalid_credentials, code='invalid_login')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password:
            return super(CustomAuthenticationForm, self).clean()

        user_model = get_user_model()
        try:
            user = user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            # Django conserva su comprobación de contraseña para usuarios desconocidos.
            return super(CustomAuthenticationForm, self).clean()

        attempt, _created = LoginAttemptDjango.objects.get_or_create(
            username=user.get_username()
        )
        attempts = LoginAttemptDjango.objects.filter(pk=attempt.pk)
        now = timezone.now()
        if attempt.bloqueado_hasta and attempt.bloqueado_hasta > now:
            user_model().set_password(password)
            raise self._locked_error(attempt.bloqueado_hasta)

        if attempt.bloqueado_hasta:
            attempts.filter(bloqueado_hasta__lte=now).update(
                intentos_fallidos=0, bloqueado_hasta=None
            )

        unlocked_attempts = attempts.filter(bloqueado_hasta__isnull=True)
        try:
            cleaned_data = super(CustomAuthenticationForm, self).clean()

        except forms.ValidationError:
            with transaction.atomic():
                unlocked_attempts.update(intentos_fallidos=F('intentos_fallidos') + 1)
                unlocked_attempts.filter(
                    intentos_fallidos__gte=self.max_failed_attempts).update(
                    bloqueado_hasta=timezone.now() + self.lockout_duration
                )

            # Volver a consultar el registro después de actualizarlo
            attempt.refresh_from_db()

            if (attempt.bloqueado_hasta and attempt.bloqueado_hasta > timezone.now()):
                raise self._locked_error(attempt.bloqueado_hasta)

            raise

        # Otro proceso pudo activar la espera durante la comprobación de la clave.
        if not unlocked_attempts.update(intentos_fallidos=0):
            self.user_cache = None
            raise self._invalid_login_error()
        return cleaned_data

    def _locked_error(self, bloqueado_hasta):
        tiempo_restante = bloqueado_hasta - timezone.now()
        segundos_totales = max(1, int(tiempo_restante.total_seconds()))

        minutos, segundos = divmod(segundos_totales, 60)

        mensaje = _(
            "Usuario bloqueado. Intente nuevamente en "
            "%(minutos)s minutos y %(segundos)s segundos."
        ) % {
                      'minutos': minutos,
                      'segundos': segundos,
                  }

        return forms.ValidationError(
            mensaje,
            code='user_locked'
        )

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
