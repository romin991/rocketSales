import django_filters
from events.models import *
from rest_framework import filters
from rest_framework import generics

class EventFilter(filters.FilterSet):
    start_time_gte = django_filters.DateTimeFilter(name="start_time", lookup_expr='gte')
    start_time_lt = django_filters.DateTimeFilter(name="start_time", lookup_expr='lt')

    class Meta:
        model = Event
        fields = ['employee', 'contact_ct', 'contact_id', 'company', 'start_time_gte', 'start_time_lt']
