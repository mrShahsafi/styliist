from django.db import models

from core.models import CommonBaseModel


class Availability(CommonBaseModel):
    stylist = models.ForeignKey(
        "scheduling.Stylist", on_delete=models.CASCADE, related_name="availabilities"
    )
    date = models.DateField()

    class Meta:
        unique_together = ("stylist", "date")

    def __str__(self):
        return f"{self.stylist.name} - {self.date}"
