from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                title_id=self.context['view'].kwargs['title_id'],
                author=request.user
            ).exists():
                raise ValidationError('Вы не можете добавить более '
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        exclude = ('title',)


class CommentCreateSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
