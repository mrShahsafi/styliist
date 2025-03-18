from django.db import models

from core.models import CommonBaseModel


class Availability(CommonBaseModel):
    stylist = models.ForeignKey(
        "scheduling.Stylist", on_delete=models.CASCADE, related_name="availabilities"
    )
    date = models.DateTimeField()

    class Meta:
        unique_together = ("stylist", "date")
        ordering = ("-date",)
        verbose_name_plural = "Availabilities"

    def __str__(self):
        return f"{self.stylist.name} - {self.date}"
