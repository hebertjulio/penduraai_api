from django.db.models import Q

from django_filters import rest_framework as filters


class ProfileFilterSet(filters.FilterSet):

    is_active = filters.BooleanFilter(method='is_active_filter')
    role__ne = filters.CharFilter(method='role__ne_filter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_active_filter(self, queryset, name, value):  # skipcq
        qs = queryset.filter(is_active=value)
        return qs

    def role__ne_filter(self, queryset, name, value):  # skipcq
        qs = queryset.filter(~Q(role=value))
        return qs

    class Meta:
        fields = [
            'role__ne', 'is_active'
        ]
