from django.contrib import admin
from django import forms
from .models import Post, Category, Feedback
from ckeditor.widgets import CKEditorWidget



# Register your models here.

# Регистрируем модели для перевода в админке




class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'category', 'get_public_date')

    list_filter = ('author', 'public_date', 'category__name')
    search_fields = ('title', 'category__name')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

    list_filter = ('name', )
    search_fields = ('name', )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_feedmaster', 'message', 'post', 'get_message_date')

    list_filter = ('user', 'message_date')
    search_fields = ('post_title', )





# Register your models here.
