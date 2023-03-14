import re

from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Feedback
from ckeditor.widgets import CKEditorWidget
from django.forms.widgets import Textarea
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя пользователя')
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='e-mail адрес')
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя')
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):
    foto = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))


    class Meta:
        model = Profile
        fields = [
            'foto',
            'email_reserve',
            'phone_num',
        ]





class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=6, help_text='Введите текст заголовка, обязательное поле до 64 символов',
                            label="Заголовок")
    content = forms.CharField(min_length=300, widget=CKEditorWidget(config_name='default'), label="Содержание")

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')
        content = re.sub('<.*?>', '', content)
        if title == content:
            raise ValidationError(
                'Содержание публикации не должно совпадать с названием'
            )
        return cleaned_data


class FeedbackForm(forms.ModelForm):
    message = forms.CharField(min_length=20, widget=Textarea(), help_text='Введите текст комментария',
                              label='Комментарий')

    class Meta:
        model = Feedback
        fields = [
            'message',
        ]
