import django_filters
from .models import LibraryUser

class LibraryUserFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='User Name')

    class Meta:
        model = LibraryUser
        fields = ['name']
