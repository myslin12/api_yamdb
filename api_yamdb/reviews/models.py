from django.db import models
from titles.models import Title
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.IntegerField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Rating(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='ratings'
    )
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0
    )
