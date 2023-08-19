from rest_framework import serializers
from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = 'username'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                {
                    'username':
                    'Нельзя использовать имя me в качестве имени пользователя.'
                }
            )
        return value

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]+$'
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username == 'me' or '':
            raise serializers.ValidationError(
                {
                    'username':
                    'Нельзя использовать имя me в качестве имени пользователя.'
                },
            )

        if not User.objects.filter(username=username, email=email):
            if User.objects.filter(username=username):
                raise serializers.ValidationError(
                    {'username': 'Username уже занят'}
                )
            if User.objects.filter(email=email):
                raise serializers.ValidationError(
                    {'email': 'email уже занято'}
                )
        return data


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
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
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
        )
