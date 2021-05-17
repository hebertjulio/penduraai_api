from django_filters import rest_framework as filters


class SheetFilterSet(filters.FilterSet):

    is_active = filters.BooleanFilter(method='is_active_filter')
    by = filters.CharFilter(method='by_filter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_active_filter(self, queryset, name, value):  # skipcq
        qs = queryset.filter(is_active=value)
        return qs

    def by_filter(self, queryset, name, value):  # skipcq
        value = 'merchant' if value == 'customer' else 'customer'
        qs = queryset.filter(**{value: self.request.user})
        qs = qs.order_by(value + '__name')
        return qs

    class Meta:
        fields = [
            'by', 'is_active'
        ]
