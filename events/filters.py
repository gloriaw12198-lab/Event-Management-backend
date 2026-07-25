import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category')
    venue = django_filters.NumberFilter(field_name='venue')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='venue__city', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['title', 'category', 'venue', 'date', 'date_from', 'date_to', 'location']