from django.urls import path
from board.views import *
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/posts/')),
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:id>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreate.as_view(), name='create_post'),
    path('posts/<int:id>/reply/', FeedCreate.as_view(), name='feed_create'),
    path('profile/replies/', FeedPost.as_view(), name='feed_post'),
    path('profile/replies/delete/<int:id>/', feed_deleter, name='feed_delete'),
    path('profile/replies/update/<int:id>/', feed_updater, name='feed_update'),
    path('profile/', profile, name='profile'),
    path('posts/<int:id>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('posts/<int:id>/delete/', PostDelete.as_view(), name='post_delete'),
]