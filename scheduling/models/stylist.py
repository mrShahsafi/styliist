from django.db import models
from django.contrib.auth import get_user_model

from core.models import CommonBaseModel

User = get_user_model()


class Stylist(CommonBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
