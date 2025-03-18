import uuid
from django.test import TestCase
from user.models import BaseUser


class BaseUserModelTest(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create(
            email="test@example.com",
            first_name="Amir",
            last_name="Shahsafi",
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "Amir")
        self.assertEqual(self.user.last_name, "Shahsafi")
        self.assertIsInstance(self.user.id, uuid.UUID)

    def test_default_values(self):
        self.assertFalse(self.user.is_staff)

    def test_full_name(self):
        self.assertEqual(self.user.full_name, "Amir Shahsafi")

    def test_str_representation(self):
        self.assertEqual(str(self.user), "test@example.com")
