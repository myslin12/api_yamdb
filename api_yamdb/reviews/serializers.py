from rest_framework import serializers
from reviews.models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
