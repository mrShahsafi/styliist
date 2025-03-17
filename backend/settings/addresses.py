import os

REDIS_URL = os.getenv(
    "REDIS_URL",
    default="redis://localhost:6379/0",
)
