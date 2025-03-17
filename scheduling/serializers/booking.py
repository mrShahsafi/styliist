from rest_framework import serializers
from ..models import Booking

from user.serializers import UserSerializer
from .availability import AvailabilityReadSerializer


class BookingReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    availability = AvailabilityReadSerializer(
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = ["id", "user", "availability", "created_at"]


class BookingWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "user", "availability", "status"]

    def validate(self, attrs):
        availability = attrs.get('availability')
        if Booking.objects.filter(availability=availability).exists():
            raise serializers.ValidationError(
                {"availability": "A booking already exists for this availability."}
            )
        return attrs
