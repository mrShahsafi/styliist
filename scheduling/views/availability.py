from django.db import IntegrityError

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..models import Availability
from ..serializers import AvailabilityReadSerializer, AvailabilityWriteSerializer

from ..filters import AvailabilityFilter


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all_actives().select_related("stylist")
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvailabilityFilter

    def get_serializer_class(self):
        return (
            AvailabilityWriteSerializer
            if self.action in ["create", "update", "partial_update", "bulk_create"]
            else AvailabilityReadSerializer
        )

    def perform_destroy(self, instance):
        instance.safe_delete(commit=True)

    @extend_schema(
        request=AvailabilityWriteSerializer(many=Availability),
        responses={201: AvailabilityReadSerializer(many=Availability)},
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        pagination_class=None,
    )
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
