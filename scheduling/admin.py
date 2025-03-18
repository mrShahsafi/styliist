from django.db import models
from django.contrib import admin
from django.forms import DateInput
from django.db import IntegrityError
from django.utils.timezone import timedelta, datetime


from .models import Stylist, Availability, Booking


class AvailabilityInline(admin.StackedInline):
    model = Availability
    extra = 0
    widgets = {"date": DateInput(attrs={"type": "date"})}
    max_num = 10


@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__email")
    inlines = [AvailabilityInline]
    raw_id_fields = ("user",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("availabilities")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "stylist", "date")
    list_filter = ("stylist", "date")
    search_fields = ("stylist__name",)
    actions = ["bulk_create_availabilities"]
    raw_id_fields = ("stylist",)
    formfield_overrides = {
        models.DateField: {"widget": DateInput(attrs={"type": "date"})}
    }
    date_hierarchy = "date"

    def bulk_create_availabilities(self, request, queryset):
        # Example: Create 10 availability entries
        try:
            availabilities = [
                Availability(
                    stylist=obj.stylist, date=datetime.now() + timedelta(days=i)
                )
                for obj in queryset
                for i in range(1, 11)
            ]
            Availability.objects.bulk_create(availabilities)
            self.message_user(
                request,
                f"Successfully created {len(availabilities)} availability records.",
            )
        except IntegrityError as e:
            self.message_user(
                request, f"Error during bulk creation: {str(e)}", level="error"
            )

    bulk_create_availabilities.short_description = (
        "Bulk Create 10 Availability Slots for Selected Stylists"
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "availability", "status")
    raw_id_fields = ("user", "availability")
    date_hierarchy = "availability__date"
