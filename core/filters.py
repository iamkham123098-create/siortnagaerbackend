"""
Custom filters for date range filtering on models.
"""

import django_filters
from .models import Activity, Event, Announcement


class ActivityFilter(django_filters.FilterSet):
    """Filter for activities with date range support."""
    from_date = django_filters.DateFilter(field_name='activity_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='activity_date', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='activity_date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='activity_date', lookup_expr='month')

    class Meta:
        model = Activity
        fields = ['from_date', 'to_date', 'year', 'month']


class EventFilter(django_filters.FilterSet):
    """Filter for events with date range and type support."""
    from_date = django_filters.DateFilter(field_name='event_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='event_date', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='event_date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='event_date', lookup_expr='month')
    event_type = django_filters.CharFilter(field_name='event_type')

    class Meta:
        model = Event
        fields = ['event_type', 'from_date', 'to_date', 'year', 'month']


class AnnouncementFilter(django_filters.FilterSet):
    """Filter for announcements with date range support."""
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='created_at', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='created_at', lookup_expr='month')
    is_pinned = django_filters.BooleanFilter(field_name='is_pinned')

    class Meta:
        model = Announcement
        fields = ['is_pinned', 'from_date', 'to_date', 'year', 'month']
