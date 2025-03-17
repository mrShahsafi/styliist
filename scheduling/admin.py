from django.contrib import admin
from django.db import models
from django.forms import DateInput
from .models import Stylist, Availability


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0
    widgets = {"date": DateInput(attrs={"type": "date"})}


@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__email")
    inlines = [AvailabilityInline]


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "stylist", "date")
    list_filter = ("stylist", "date")
    search_fields = ("stylist__name",)
    formfield_overrides = {
        models.DateField: {"widget": DateInput(attrs={"type": "date"})}
    }
