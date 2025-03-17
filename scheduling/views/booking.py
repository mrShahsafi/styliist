from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from ..models import Booking
from ..serializers import BookingReadSerializer, BookingWriteSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user", "availability")

    def get_serializer_class(self):
        return (
            BookingWriteSerializer
            if self.action in ["create", "update", "partial_update"]
            else BookingReadSerializer
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        availability = serializer.validated_data["availability"]
        booking = Booking.create_booking(user, availability)
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
