from reviews.models import Comment, Review
from .serializers import CommentCreateSerializer, ReviewCreateSerializer
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from titles.models import Title
from reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title)


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
