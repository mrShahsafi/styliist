from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from user.models import BaseUser


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        user = BaseUser.objects.create_superuser(
            email="test@example.com",
            password="VerryStrongPass123098754321213",
        )
        self.user = user
        BaseUser.objects.create(
            email="ordinary@example.com",
            password="VerryStrongPass123098754321213",
        )

    def test_register(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "password": "Amir2187481",
            "email": "test@test.com",
        }
        response = self.client.post("/users/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_email_exists_register(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "password": "Amir2187481",
            "email": "test@example.com",
        }
        response = self.client.post("/users/", data=data)
        self.assertEqual(response.status_code, 400)

    def test_password_too_common_register(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "email": "test@test.com",
            "password": "abc",
        }
        response = self.client.post("/users/", data=data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        data = {
            "email": "test@example.com",
            "password": "VerryStrongPass123098754321213",
        }
        response = self.client.post("/users/auth/token/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_no_body_login(self):
        data = {}
        response = self.client.post("/users/auth/token/", data=data)
        self.assertEqual(response.status_code, 400)
