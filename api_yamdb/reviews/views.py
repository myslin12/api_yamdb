from reviews.models import Comment, Review
from .serializers import CommentCreateSerializer, ReviewCreateSerializer
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from reviews.models import Rating, Review, Title
from api.pagination import ApiPagination
from django.db.models import Avg
from api.permissions import CommentRewiewPermission


class ReviewViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()
    pagination_class = ApiPagination
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        serializer.save(title=title, author=author)
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
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        author = self.request.user
        serializer.save(review=review, author=author)
