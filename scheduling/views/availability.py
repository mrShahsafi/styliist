from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Availability
from ..serializers import AvailabilityReadSerializer, AvailabilityWriteSerializer


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.select_related("stylist")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date", "stylist"]

    def get_serializer_class(self):
        return (
            AvailabilityWriteSerializer
            if self.action in ["create", "update", "partial_update"]
            else AvailabilityReadSerializer
        )
