from django.db import models


class Title(models.Model):
    '''Модель произведений.'''
    name = models.CharField(max_length=256)
    year = models.IntegerField()
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

    def __str__(self):
        return self.name


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
