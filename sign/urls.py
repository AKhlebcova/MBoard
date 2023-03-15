from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup, user_code

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', signup, name='signup'),
    path('signup/activate/', user_code, name='activate'),
]
