from random import randint, choice
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import timedelta, datetime

from faker import Faker

from scheduling.models import Stylist, Availability, Booking


User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with initial data for Users, Stylists, Availability, and Bookings"

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Creating the Superuser..")
        try:
            User.objects.create_superuser(email="x@x.com", password="2187481")
        except IntegrityError:
            pass

        self.stdout.write(f"Seeding Users..")
        users = [
            User.objects.create_user(email=fake.email(), password="test123")
            for _ in range(20)
        ]
        for user in users:
            self.stdout.write(f"Created User: {user.email}")

        self.stdout.write(f"Seeding Stylists..")
        stylist_users = random.sample(users, min(10, len(users)))
        stylists = []

        for user in stylist_users:
            stylist, created = Stylist.objects.get_or_create(
                user=user, defaults={"name": fake.name()}
            )
            stylists.append(stylist)
            self.stdout.write(
                f"{'Created' if created else 'Existing'} Stylist: {stylist.name} (User: {stylist.user.email})"
            )

        self.stdout.write(f"Seeding Availabilities..")
        availabilities = [
            Availability.objects.create(
                stylist=choice(stylists),
                date=datetime.now() + timedelta(days=randint(1, 30)),
            )
            for _ in range(30)
        ]
        for availability in availabilities:
            self.stdout.write(
                f"Created Availability: {availability.date} (Stylist: {availability.stylist.name})"
            )

        self.stdout.write(f"Seeding Bookings..")

        available_slots = list(availabilities)
        bookings = []

        for _ in range(min(len(available_slots), 15)):
            availability = available_slots.pop()
            user = choice(users)
            status = choice(
                [
                    Booking.Statuses.PENDING,
                    Booking.Statuses.REJECTED,
                    Booking.Statuses.ACCEPTED,
                    Booking.Statuses.CANCELED,
                ]
            )

            booking = Booking.objects.create(
                user=user, availability=availability, status=status
            )
            bookings.append(booking)

            self.stdout.write(
                f"Created Booking: {booking.status} (User: {booking.user.email}, Availability: {booking.availability.date})"
            )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
