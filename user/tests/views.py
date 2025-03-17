import json
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from user.models import BaseUser

from core.responses import (
    USER_WITH_MAIL_ALREADY_EXIST_EN,
    USER_WITH_MOBILE_ALREADY_EXIST_EN,
    VALIDATION_ERR_EN,
    REQUIRED_FIELD_EN,
)


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        BaseUser.objects.create_superuser(
            email="test@example.com",
            password="VerryStrongPass123098754321213",
        )

        BaseUser.objects.create(
            email="ordinary@example.com",
            password="VerryStrongPass123098754321213",
            whatsapp_number="12345678910",
        )

    def test_register(self):
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "password": "Amir2187481",
            "email": "test@test.com",
        }
        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_email_exists_register(self):
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "password": "Amir2187481",
            "email": "test@test.com",
        }
        response = self.client.post("/user/", data=data)
        expected_error_message = {"email": USER_WITH_MAIL_ALREADY_EXIST_EN}
        self.assertEqual(response.status_code, 400) and self.assertEqual(
            response.content, expected_error_message
        )

    def test_password_too_common_register(self):
        data = {
            "first_name": "admin first name",
            "last_name": "admin last name",
            "email": "test@test.com",
            "password": "qwerty",
        }
        response = self.client.post("/user/", data=data)
        expected_error_message = {
            "password": "Ensure this field has at least 8 characters."
        }
        self.assertEqual(response.status_code, 400) and self.assertEqual(
            response.content, expected_error_message
        )

    def test_login(self):
        data = {
            "email": "test@example.com",
            "password": "VerryStrongPass123098754321213",
        }
        response = self.client.post("/auth/token/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_no_body_login(self):

        data = {"data": "I am the nightmare.."}
        response = self.client.post("/auth/token/", data=data)

        expected_error_message = {
            "email": REQUIRED_FIELD_EN,
            "password": REQUIRED_FIELD_EN,
            "error": VALIDATION_ERR_EN,
            "code": 400,
        }
        self.assertEqual(response.status_code, 400) and self.assertEqual(
            response.content, expected_error_message
        )
