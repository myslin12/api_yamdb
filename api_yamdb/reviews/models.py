from django.db import models
from titles.models import Title
from rest_framework import serializers
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
    review_id = models.SlugField()
    text = serializers.CharField(max_length=255)
    author = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
