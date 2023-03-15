from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CodeForm(forms.ModelForm):
    code = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Код:')
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                             label='e-mail адрес')

    class Meta:
        model = User
        fields = ['email', ]


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
# Create your models here.
