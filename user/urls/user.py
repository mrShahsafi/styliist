from rest_framework import routers

from ..views import (
    UserViewSetApi,
)

router = routers.SimpleRouter()
router.register(r"users", UserViewSetApi, basename="user")


urlpatterns = router.urls
