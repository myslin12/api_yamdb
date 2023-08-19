from django.core.validators import RegexValidator
from django.db.models import Q

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


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email')

    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='В username может состоять из букв, цифр и знаков: @ . + - _',
        code='invalid_username'
    )

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

        existing_user_with_username = (
            User.objects.filter(username=username)
            .exclude(email=email)
            .first()
        )
        if existing_user_with_username:
            raise serializers.ValidationError(
                {'username': 'Имя пользователя занято.'}
            )

        existing_user_with_email = (
            User.objects.filter(email=email)
            .exclude(username=username)
            .first()
        )
        if existing_user_with_email:
            raise serializers.ValidationError({'email': 'Почта уже занята.'})

        self.username_validator(username)

        return data

    def create(self, validated_data):
        existing_user = User.objects.filter(
            Q(username=validated_data['username'])
            | Q(email=validated_data['email'])
        ).first()

        if existing_user:
            return existing_user

        user = User.objects.create_user(**validated_data)
        return user


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
