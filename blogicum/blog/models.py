from django.db import models

from core.models import PublishedModel

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(PublishedModel):
    """Модель Категории."""
    title = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название категории, не более 256 символов'
    )
    slug = models.SlugField(
        unique=True,
        max_length=64,
        verbose_name='Слаг',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание категории, текстовое поле'
    )

    class Meta:
        verbose_name = 'объект "Категория"'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    """Модель Местоположения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название местоположения, не более 256 символов',
    )

    class Meta:
        verbose_name = 'объект "Местоположение"',
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    """Модель Публикации."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Автор поста'
    )
    title = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Заголовок поста, не более 256 символов',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата',
        help_text='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='post',
        verbose_name='Категория',
        help_text='Название категории',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='post',
        verbose_name='Местоположение',
        help_text='Название местоположения',
    )

    class Meta:
        verbose_name = 'объект "Публикация"'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title