from reviews.models import Comment, Review
from .serializers import CommentCreateSerializer, ReviewCreateSerializer
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from titles.models import Title
from reviews.models import Rating, Review
from api.pagination import ApiPagination
from django.db.models import Avg


class ReviewViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()
    pagination_class = ApiPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title)
        self.update_average_rating(title)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.update_average_rating(instance.title)

    def update_average_rating(self, title):
        average_rating = Review.objects.filter(
            title=title
        ).aggregate(Avg('score'))['score__avg']
        rating, _ = Rating.objects.get_or_create(title=title)
        rating.average_rating = average_rating or 0
        rating.save()


class CommentViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review)
