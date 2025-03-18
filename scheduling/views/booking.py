from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..models import Booking
from ..serializers import BookingReadSerializer, BookingWriteSerializer

User = get_user_model()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all_actives().select_related("user", "availability")

    def get_serializer_class(self):
        return (
            BookingWriteSerializer
            if self.action in ["create", "update", "partial_update"]
            else BookingReadSerializer
        )

    @extend_schema(
        request=BookingWriteSerializer,
        responses={
            201: OpenApiResponse(
                description="Booking Reserved",
                examples=[
                    OpenApiExample(
                        "Booking Created",
                        summary="Successful Booking Creation",
                        value={"message": "Booking Reserved with task ID: 12345"},
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Booking not Reserved",
                examples=[
                    OpenApiExample(
                        "Booking Failed",
                        summary="Failed Booking Creation",
                        value={
                            "availability": [
                                "A booking already exists for this availability."
                            ]
                        },
                    )
                ],
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        availability = serializer.validated_data["availability"]
        booking_task_id = Booking.create_booking(user, availability)
        return Response(
            {"message": f"Booking Reserved with task ID: {booking_task_id}"},
            status=status.HTTP_201_CREATED,
        )

    def perform_destroy(self, instance):
        instance.safe_delete(commit=True)
