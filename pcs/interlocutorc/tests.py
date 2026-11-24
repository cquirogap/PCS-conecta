# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .forms import CustomAuthenticationForm
from .models import LoginAttemptDjango


class WebLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('cuenta-prueba', password='Clave de prueba')

    def submit(self, username, password):
        form = CustomAuthenticationForm(data={'username': username, 'password': password})
        form.is_valid()
        return form

    def test_failed_attempts_block_even_the_right_password_until_expiry(self):
        first_failure = self.submit(self.user.username, 'incorrecta')
        for _ in range(CustomAuthenticationForm.max_failed_attempts - 1):
            self.assertFalse(self.submit(self.user.username, 'incorrecta').is_valid())

        attempt = LoginAttemptDjango.objects.get(username=self.user.username)
        self.assertEqual(attempt.intentos_fallidos, CustomAuthenticationForm.max_failed_attempts)
        self.assertGreater(attempt.bloqueado_hasta, timezone.now())

        blocked = self.submit(self.user.username, 'Clave de prueba')
        self.assertFalse(blocked.is_valid())
        self.assertEqual(blocked.non_field_errors(), first_failure.non_field_errors())
        original_expiry = attempt.bloqueado_hasta
        attempt.refresh_from_db()
        self.assertEqual(attempt.bloqueado_hasta, original_expiry)

        attempt.bloqueado_hasta = timezone.now() - timedelta(seconds=1)
        attempt.save(update_fields=['bloqueado_hasta'])
        self.assertTrue(self.submit(self.user.username, 'Clave de prueba').is_valid())
        attempt.refresh_from_db()
        self.assertEqual(attempt.intentos_fallidos, 0)
        self.assertIsNone(attempt.bloqueado_hasta)

    def test_unknown_and_inactive_accounts_use_same_message(self):
        unknown = self.submit('cuenta-inexistente', 'incorrecta')
        self.assertFalse(unknown.is_valid())
        self.assertFalse(LoginAttemptDjango.objects.filter(username='cuenta-inexistente').exists())

        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        inactive = self.submit(self.user.username, 'Clave de prueba')
        self.assertFalse(inactive.is_valid())
        self.assertEqual(inactive.non_field_errors(), unknown.non_field_errors())

    def test_successful_login_resets_consecutive_failures(self):
        self.assertFalse(self.submit(self.user.username, 'incorrecta').is_valid())
        self.assertTrue(self.submit(self.user.username, 'Clave de prueba').is_valid())
        attempt = LoginAttemptDjango.objects.get(username=self.user.username)
        self.assertEqual(attempt.intentos_fallidos, 0)

    def test_web_view_applies_lockout_and_allows_login_after_expiration(self):
        credentials = {'username': self.user.username, 'password': 'incorrecta'}
        for _ in range(CustomAuthenticationForm.max_failed_attempts):
            self.assertContains(self.client.post('/login/', credentials), 'Revisa tus datos')

        credentials['password'] = 'Clave de prueba'
        self.assertContains(self.client.post('/login/', credentials), 'Revisa tus datos')
        LoginAttemptDjango.objects.filter(username=self.user.username).update(
            bloqueado_hasta=timezone.now() - timedelta(seconds=1)
        )
        response = self.client.post('/login/', credentials)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('_auth_user_id'), str(self.user.pk))
