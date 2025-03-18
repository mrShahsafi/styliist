from django.contrib.auth import get_user_model

from rest_framework import serializers
from ..models import Booking, Availability

from user.serializers import UserSerializer
from .availability import AvailabilityReadSerializer

User = get_user_model()


class BookingReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    availability = AvailabilityReadSerializer(
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = ["id", "user", "availability", "created_date", "updated_date"]


class BookingWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    availability = serializers.PrimaryKeyRelatedField(
        queryset=Availability.objects.all()
    )

    class Meta:
        model = Booking
        fields = ["id", "user", "availability", "status"]

    def validate(self, attrs):
        availability = attrs.get("availability")
        if Booking.objects.filter(availability=availability).exists():
            raise serializers.ValidationError(
                {"availability": "A booking already exists for this availability."}
            )
        return attrs
