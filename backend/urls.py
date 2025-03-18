from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# DRF
from rest_framework import routers

# swagger
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL, SITE_NAME

# from patches import routers

router = routers.DefaultRouter()

# Admin panel display names
admin.site.site_header = SITE_NAME
admin.site.site_title = f"{SITE_NAME} Portal"
admin.site.index_title = f"Welcome to {SITE_NAME} Portal"

# API_V1 = "api/v1"


apis = [
    path("users/", include("user.urls")),
    path("scheduling/", include("scheduling.urls")),
    path("", include(router.urls)),
    # Swagger APIs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]


template_urls = [
    path("admin/", admin.site.urls),
]

urlpatterns = apis + template_urls

if DEBUG:
    import debug_toolbar

    def trigger_error(request):
        division_by_zero = 1 / 0

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        # Visiting this route will trigger an error that will be captured by Sentry.
        path("sentry-debug/", trigger_error),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
