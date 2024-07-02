from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from . import constants


User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created_at', )


class Location(PublishedModel):
    name = models.CharField(
        'Название места', max_length=constants.MAX_FIELD_LENGTH)

    class Meta(PublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:constants.REPRESENTATION_LENGTH]


class Category(PublishedModel):
    title = models.CharField(
        'Заголовок', max_length=constants.MAX_FIELD_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        max_length=constants.MAX_FIELD_LENGTH,
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:constants.REPRESENTATION_LENGTH]


class Post(PublishedModel):
    title = models.CharField(
        'Заголовок', max_length=constants.MAX_FIELD_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно '
            'делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='post_images/',
        blank=True,
    )

    class Meta(PublishedModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', ) + PublishedModel.Meta.ordering

    def __str__(self):
        return self.title[:constants.REPRESENTATION_LENGTH]

    def get_absolute_url(self):
        return reverse('post_detail', args=self.id)


class Comment(PublishedModel):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        # Поменяла! Но, разве ниже мы не дублируем ForeignKey в
        # одной и той же модели?
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',  # Вот тут.
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = PublishedModel.Meta.ordering

    def __str__(self) -> str:
        return f'{self.author}: {self.text[:constants.COMMENT_PREVIEW_LENGTH]}'
