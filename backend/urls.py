from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL, SITE_NAME

# Admin panel display names
admin.site.site_header = SITE_NAME
admin.site.site_title = f"{SITE_NAME} Portal"
admin.site.index_title = f"Welcome to {SITE_NAME} Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("scheduling", include("scheduling.urls")),
]

if DEBUG:
    import debug_toolbar

    def trigger_error(request):
        division_by_zero = 1 / 0

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        # Visiting this route will trigger an error that will be captured by Sentry.
        path("sentry-debug/", trigger_error),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
