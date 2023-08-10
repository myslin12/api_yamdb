from django.db import models
from titles.models import Title
from rest_framework import serializers


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = serializers.CharField(max_length=255)
    author = models.IntegerField()
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Comment(models.Model):
    review_id = models.SlugField()
    text = serializers.CharField(max_length=255)
    author = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
