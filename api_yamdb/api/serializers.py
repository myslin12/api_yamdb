from rest_framework import serializers
from titles.models import Title, Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        # Не забыть добавить поле рейтинга
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)