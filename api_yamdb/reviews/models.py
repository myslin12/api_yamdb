import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


USER_ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    """Класс для пользовательской модели."""
    email = models.EmailField(
        'email address',
        blank=False,
        unique=True,
        max_length=254,
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default='user',
    )
    code = models.CharField(
        max_length=50,
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )

    def __str__(self):
        return self.username


class Genre(models.Model):
    '''Модель жанров.'''
    slug = models.SlugField(unique=True, max_length=50)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Category(models.Model):
    '''Модель категории.'''
    slug = models.SlugField(unique=True, max_length=50)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель произведений.'''
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                datetime.datetime.now().year,
                message="Год не должен быть больше текущего."
            )
        ]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='titles'
    )

    @property
    def rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            average_score = reviews.aggregate(models.Avg('score'))['score__avg']
            return round(average_score, 1)
        return None

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']


class Rating(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='ratings'
    )
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0
    )
