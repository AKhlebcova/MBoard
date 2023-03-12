from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from ckeditor.widgets import CKEditorWidget
# widget=CKEditorWidget(config_name='awesome_ckeditor')


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]

        widget = {
            'author': CKEditorWidget(config_name='default'),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     text = cleaned_data.get('text')
    #     title = cleaned_data.get('title')
    #     if title == text:
    #         raise ValidationError(
    #             _('Содержание публикации не должно совпадать с названием')
    #         )
    #
    #     return cleaned_data
