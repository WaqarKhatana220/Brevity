import django_filters


class SubscribersListingFilter(django_filters.FilterSet):
    author_id = django_filters.NumberFilter(method='filter_by_author_id')

    class Meta:
        fields = ['author_id']

    def filter_by_author_id(self, queryset, name, value):
        if value:
            return queryset.filter(author__id=value)
        else:
            return queryset
