from random import randint

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import BaseRegisterForm, CodeForm
from django.template.loader import render_to_string
from board.models import OnetimeCode
from django.contrib import messages


def signup(request):
    if request.method == 'GET':
        form = BaseRegisterForm()
        return render(request, 'sign/signup.html', {'form': form})

    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            code = str(randint(1000, 9999))
            subject = 'Активация аккаунта на сайте'
            OnetimeCode.objects.create(short_code=code, user=user)

            context = {
                'user': user,
                'code': code,
            }
            html_content = render_to_string('active_email.html', context)
            email = form.cleaned_data.get('email')

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email='annakhlebtsova@yandex.ru',
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, 'Вам на почту отправлен код подтверждения регистрации')
            return redirect('/sign/signup/activate/')
        else:
            form = BaseRegisterForm()
            return render(request, 'sign/signup.html', {'form': form})


def user_code(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get('email'))
            code_obj = OnetimeCode.objects.get(user=user)
            code = code_obj.short_code
            code_use = form.cleaned_data.get('code')
            if code == code_use:
                user.is_active = True
                user.save()
                code_obj.delete()
                return redirect('/posts/')
            else:
                messages.error(request, 'Неверный код!')
        else:
            messages.error(request, 'Неправильно заполнена форма!')
    form = CodeForm()
    return render(request, 'sign/activate.html', {'form': form})

# Create your views here.
