from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Stylist, Availability
from ..serializers import StylistWriteSerializer, StylistReadSerializer


class StylistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stylist.objects.all_actives().prefetch_related("availabilities")

    def get_serializer_class(self):
        return (
            StylistWriteSerializer
            if self.action in ["create", "update", "partial_update"]
            else StylistReadSerializer
        )
