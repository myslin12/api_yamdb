from django_filters import CharFilter, FilterSet, NumberFilter
from reviews.models import Title, User


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    year = NumberFilter(field_name='year', lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']


class UserFilter(FilterSet):
    search = CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['search']
