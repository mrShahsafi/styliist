from django.urls import path, include

urlpatterns = [
    path("", include("scheduling.urls.availability")),
    path("", include("scheduling.urls.stylist")),
    path("", include("scheduling.urls.booking")),
]
