from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class AuthFlowTests(TestCase):
    def setUp(self):
        User.objects.create_user("eve","eve@example.com","pass")

    def test_login_page_renders(self):
        r = self.client.get(reverse("login"))
        self.assertEqual(r.status_code, 200)

    def test_password_reset_sends_email(self):
        r = self.client.post(reverse("password_reset"), {"email": "eve@example.com"})
        self.assertRedirects(r, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset", mail.outbox[0].body.lower())
