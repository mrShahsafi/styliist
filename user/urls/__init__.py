from django.urls import path, include

urlpatterns = [
    path("", include("users.urls.user")),
    path("", include("users.urls.auth")),
]
