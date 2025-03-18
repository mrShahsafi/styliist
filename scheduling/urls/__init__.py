from django.urls import path, include

from .stylist import urlpatterns as stylist_urlpatterns
from .availability import urlpatterns as availability_urlpatterns
from .booking import urlpatterns as booking_urlpatterns

urlpatterns = [
    path("", include(availability_urlpatterns)),
    path("", include(stylist)),
    path("", include(booking)),
]
