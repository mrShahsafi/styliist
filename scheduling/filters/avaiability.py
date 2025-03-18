from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from ..models import Availability


class AvailabilityFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = Availability
        fields = ["date", "stylist"]
