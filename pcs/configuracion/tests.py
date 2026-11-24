# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from smtplib import SMTPException

from django.contrib.auth.models import User
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.test import TestCase, override_settings
from django.urls import Resolver404, resolve, reverse


class FailingRecoveryEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        raise SMTPException('Fallo de prueba')


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordRecoveryTests(TestCase):
    path = '/registrar/olvidar_contrasena/'

    def setUp(self):
        self.user = User.objects.create_user(
            'cuenta-prueba', email='cuenta@example.com', password='Clave original'
        )

    def test_registered_and_unregistered_addresses_get_the_same_confirmation(self):
        registered = self.client.post(self.path, {'email': self.user.email})
        unregistered = self.client.post(self.path, {'email': 'otra@example.com'})

        self.assertEqual(registered.status_code, 302)
        self.assertEqual(unregistered.status_code, 302)
        self.assertEqual(registered['Location'], unregistered['Location'])

        confirmation = self.client.get(registered['Location'])
        self.assertContains(confirmation, 'Si existe una cuenta asociada')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        temporary_password = re.search(r'desde tu perfil: (\w+)\.', mail.outbox[0].body).group(1)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(temporary_password))

    @override_settings(EMAIL_BACKEND='configuracion.tests.FailingRecoveryEmailBackend')
    def test_failed_delivery_does_not_replace_the_password(self):
        response = self.client.post(self.path, {'email': self.user.email})
        self.assertRedirects(response, self.path + '?solicitud=recibida')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Clave original'))

    def test_missing_email_gets_the_generic_confirmation(self):
        response = self.client.post(self.path, {})
        self.assertRedirects(response, self.path + '?solicitud=recibida')
        self.assertEqual(len(mail.outbox), 0)


class AdministrationRouteTests(TestCase):
    def test_native_console_is_removed_and_application_routes_still_resolve(self):
        with self.assertRaises(Resolver404):
            resolve('/admin123/login/')
        self.assertEqual(reverse('login'), '/login/')
        self.assertEqual(resolve('/administracion/').url_name, 'admin-panel')
        self.assertTrue(callable(resolve('/login_api/').func))
