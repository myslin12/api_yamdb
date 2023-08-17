from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from .permissions import GenresTitlesPermission


class ListCreateDestroyMixin(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
):
    permission_classes = (GenresTitlesPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
