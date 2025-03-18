from rest_framework import serializers

from .availability import (
    AvailabilityWriteSerializer,
    AvailabilityReadExcludeStylistSerializer,
)

from ..models import Stylist


class StylistReadSerializer(serializers.ModelSerializer):
    availabilities = AvailabilityReadExcludeStylistSerializer(many=True, read_only=True)

    class Meta:
        model = Stylist
        fields = ["id", "name", "availabilities"]


class StylistWriteSerializer(serializers.ModelSerializer):
    availabilities = AvailabilityWriteSerializer(many=True, read_only=True)

    class Meta:
        model = Stylist
        fields = ["id", "name", "availabilities"]
