from django.db import models
from django.contrib.auth import get_user_model

from django_q.tasks import async_task


from ..models import Availability

from core.models import CommonBaseModel

User = get_user_model()


class Booking(CommonBaseModel):
    class Statuses(models.IntegerChoices):
        PENDING = 0, "Pending"
        ACCEPTED = 1, "Accepted"
        REJECTED = 2, "Rejected"
        CANCELED = 3, "Canceled"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    availability = models.OneToOneField(
        Availability, on_delete=models.CASCADE, related_name="booking"
    )
    status = models.IntegerField(
        choices=Statuses.choices,
        default=Statuses.PENDING,
    )

    @classmethod
    def create_booking(cls, user, availability):
        return async_task(cls._async_create_booking, user.id, availability.id)

    @staticmethod
    def _async_create_booking(user_id, availability_id):
        user = User.objects.get(id=user_id)
        availability = Availability.objects.get(id=availability_id)
        Booking.objects.create(user=user, availability=availability)

    def __str__(self):
        return f"{self.user} booked {self.availability}"
