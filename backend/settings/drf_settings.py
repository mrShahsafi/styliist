from datetime import timedelta
from .base import SITE_NAME

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
    "PAGE_SIZE": 9,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "core.errors.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

REGISTRATION = {
    "TOKEN_EXPIRE": 1200,  # 20 Minuets
    "REFRESH_LINK_LIMIT": 1200,  # 20 Minuets
}

FORGOT_PASSWORD = {
    "TOKEN_EXPIRE": timedelta(minutes=30),
    "RESEND_TOKEN_AVAILABLE_AT": timedelta(minutes=2),
}

# REMEMBERED_USER_ACCESS_LIFETIME = datetime.timedelta(days=50)
SPECTACULAR_SETTINGS = {
    "TITLE": f"{SITE_NAME} Project API",
    "DESCRIPTION": "Finding and reserving homes",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}
