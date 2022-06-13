from datetime import timedelta
import datetime

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import SET_NULL, CASCADE


# 1. Разрабатываем каталог книг, у каждой книги обязательно есть автор, и он может быть только один.
     #(!!!чтобы не копипастить код во 2-е задание я сделал упрощенное представление, а во втором уже старался прокачать)
from django.utils import timezone


class Writer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dob = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '1_Author'


class Publication(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Writer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '1_Book'

# 2. Разработать книжную библиотеку. Храним книги, храним авторов, книгу могут написать несколько соавторов.
#    Xраним кто брал книги, и доступна ли книга сейчас.

class Member(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=100, blank=True)
    date_of_joining = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '2_Member'


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dob = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '2_Author'

class Book(models.Model):
    ENGLISH = 'EN'
    UKRAINIAN = 'UA'
    RUSSIAN = 'RU'
    CHINESE = 'CH'
    SPANISH = 'SP'
    OTHER = 'OT'
    LANGUAGE_CHOICES = [
        (ENGLISH, 'English'),
        (UKRAINIAN, 'Ukrainian'),
        (RUSSIAN, 'Russian'),
        (CHINESE, 'Chinese'),
        (SPANISH, 'Spanish'),
        (OTHER, 'Other'),
    ]
    title = models.CharField(max_length=250)
    author = models.ManyToManyField(Author)
    #  хотел сделать Автора обязательным, но прочитал что в случае M2M такая валидация делается на уровне контроллера
    original_lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=OTHER)
    year_of_public = models.DateField()
    date_of_getting = models.DateField(auto_now=True)
    is_free = models.BooleanField(default=True)
    date_of_status_changing = models.DateField(auto_now_add=True)
    is_taken_by = models.ForeignKey(Member, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '2_Book'

# Разработать набор моделей, для сайта-блога, на котором можно выставлять свои статьи,
#  комментировать чужие, ставить лайк и дизлайк статье, и комментарию.
#  3.1* Доделать так, что бы связи позволяли комментировать комментарии.
#  3.2* Сделать лайки через GenericForeignKey

class Profile(models.Model):
    login = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    dob = models.DateField()
    date_of_registration = models.DateField(auto_now=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '3_User'

class Article(models.Model):
    author = models.ForeignKey(Profile, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_of_writing = models.DateField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    date_of_moderation = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    likes = GenericRelation('Like')
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '3_Article'

class Comment(models.Model):
    comment = models.TextField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=CASCADE)
    date = models.DateTimeField(auto_now=False)
    likes = GenericRelation('Like')
    comments = GenericRelation('self')
    limit = models.Q(app_label='myapp', model='article') | models.Q(app_label='myapp', model='comment')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.author}'s comment for '{self.liked_object}': {self.comment[:15]}"

    def save(self, **kwargs):
        def delta_years(dt, years):
            try:
                result = datetime.datetime(dt.year + years, dt.month, dt.day, dt.hour, dt.minute, dt.second,
                                           dt.microsecond,
                                           dt.tzinfo)
            except ValueError:
                result = datetime.datetime(dt.year + years, dt.month, dt.day - 1, dt.hour, dt.minute, dt.second,
                                           dt.microsecond, dt.tzinfo)
            return result

        if not self.id:
            self.date = delta_years(timezone.now(), -1)
        super().save(**kwargs)

    class Meta:
        verbose_name = '3_Comment'
        ordering = ["-id"]

class Like(models.Model):
    LIKE_OPTIONS = (
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    type = models.CharField(max_length=1, choices=LIKE_OPTIONS, default='L')
    author = models.ForeignKey(Profile, on_delete=CASCADE)
    date = models.DateTimeField(auto_now=True)
    limit = models.Q(app_label='myapp', model='article') | models.Q(app_label='myapp', model='comment')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.author}'s {self.type} for {self.liked_object}"

    class Meta:
        verbose_name = '3_Like'
