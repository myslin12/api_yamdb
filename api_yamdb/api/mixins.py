from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyMixin(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
