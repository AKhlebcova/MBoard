from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    public_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, verbose_name='Категория')
    title = models.CharField(max_length=64, unique=True, verbose_name='Заголовок')
    content = RichTextField(blank=False, verbose_name='Содержание объявления')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}'

    def get_author(self):
        return self.author.username

    def get_public_date(self):
        return self.public_date.strftime('%Y-%m-%d')

    def post_preview(self):
        if len(self.content) <= 300:
            return f'{self.content}...'
        return f'{self.content[0:300]}...'


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.CharField(max_length=700, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message_date = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False, verbose_name='Комментарий принят автором')

    def get_message_date(self):
        return self.message_date.strftime('%Y-%m-%d')

    def get_feedmaster(self):
        return self.user.username

    def reply_preview(self):
        if len(self.message) <= 15:
            return f'{self.message}...'
        return f'{self.message[0:15]}...'


class OnetimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    short_code = models.CharField(max_length=8, verbose_name='Проверочный код')
    create_date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    photo = models.ImageField(default='default.png', upload_to='profile_images', verbose_name='Аватар')

    email_reserve = models.EmailField(verbose_name='Дополнительный email', blank=True)
    phone_num = models.CharField(max_length=25, verbose_name='Номер телефона', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

# Create your models here.
