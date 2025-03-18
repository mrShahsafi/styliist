from django.test import TestCase
from django.contrib.auth import get_user_model
from scheduling.models import Stylist, Availability, Booking
from datetime import date

User = get_user_model()


class StylistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user1@test.com", password="test123")
        self.stylist = Stylist.objects.create(user=self.user, name="TestStylist 1")

    def test_create_stylist(self):
        self.assertEqual(self.stylist.user, self.user)
        self.assertEqual(self.stylist.name, "TestStylist 1")
        self.assertEqual(Stylist.objects.count(), 1)


class AvailabilityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user2@test.com", password="test123")
        self.stylist = Stylist.objects.create(user=self.user, name="TestStylist 2")
        self.availability = Availability.objects.create(
            stylist=self.stylist, date=date(2025, 3, 18)
        )

    def test_create_availability(self):
        self.assertEqual(self.availability.stylist, self.stylist)
        self.assertEqual(self.availability.date, date(2025, 3, 18))
        self.assertEqual(Availability.objects.count(), 1)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="client@test.com", password="test123"
        )
        self.stylist_user = User.objects.create_user(
            email="user4@test.com", password="test123"
        )
        self.stylist = Stylist.objects.create(
            user=self.stylist_user, name="TestStylist 3"
        )
        self.availability = Availability.objects.create(
            stylist=self.stylist, date=date(2025, 3, 19)
        )

    def test_create_booking(self):
        booking = Booking.objects.create(user=self.user, availability=self.availability)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.availability, self.availability)
        self.assertEqual(Booking.objects.count(), 1)
