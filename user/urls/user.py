from django.urls import path, include
from rest_framework import routers

from ..views import (
    UserViewSetApi,
)

router = routers.DefaultRouter()
router.register(r"", UserViewSetApi, basename="user")


urlpatterns = [
    path("", include(router.urls)),
]
