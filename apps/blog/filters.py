import django_filters


class BlogListingFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(method='filter_by_state')
    id = django_filters.CharFilter(method='filter_by_id')

    class Meta:
        fields = ['state']

    def filter_by_state(self, queryset, name, value):
        if value:
            return queryset.filter(state=value)
        else:
            return queryset
        
    def filter_by_id(self, queryset, name, value):
        if value:
            return queryset.filter(id=value)
        else:
            return queryset
