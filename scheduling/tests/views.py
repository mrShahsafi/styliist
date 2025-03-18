from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from scheduling.models import Stylist, Availability, Booking
from datetime import datetime

User = get_user_model()


class StylistViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="alice@example.com", password="test123"
        )
        self.client.force_authenticate(user=self.user)
        self.stylist = Stylist.objects.create(user=self.user, name="Alice the Stylist")
        self.url = reverse("stylist-list")

    def test_list_stylists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "Alice the Stylist")


class AvailabilityViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="bob@example.com", password="test123"
        )
        self.client.force_authenticate(user=self.user)
        self.stylist = Stylist.objects.create(user=self.user, name="Bob the Barber")
        self.availability = Availability.objects.create(
            stylist=self.stylist, date=datetime(2025, 3, 18, 10, 0, 0)
        )
        self.url = reverse("availability-list")

    def test_list_availabilities(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["date"], "2025-03-18T10:00:00Z")


class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="charlie@example.com", password="test123"
        )
        self.stylist_user = User.objects.create_user(
            email="dave@example.com", password="test123"
        )
        self.client.force_authenticate(user=self.client_user)
        self.stylist = Stylist.objects.create(
            user=self.stylist_user, name="Dave the Designer"
        )
        self.availability = Availability.objects.create(
            stylist=self.stylist, date=datetime(2025, 3, 19, 14, 30, 0)
        )
        self.url = reverse("booking-list")
        self.booking_data = {
            "user": self.client_user.id,
            "availability": self.availability.id,
        }

    def test_create_booking(self):
        response = self.client.post(self.url, self.booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
