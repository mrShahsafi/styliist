from rest_framework import serializers
from ..models import Stylist, Availability


class AvailabilityReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["id", "date"]


class AvailabilityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"
