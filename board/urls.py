from django.urls import path
from board.views import *
from django.views.generic.base import RedirectView
# from django.views.decorators.cache import cache_page

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


    # path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete_article'),
    # path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    # path('index/', IndexView.as_view(), name='user_index'),
    # path('upgrade/', upgrade_me, name='upgrade'),
    # path('news/category/<int:pk>', CategoryPostList.as_view(), name='posts_category'),
    # path('news/category/<int:pk>/subscriber', subscriber, name='subscriber'),
    # path('start/', start, name='start'),
    # # path('log/', log, name='logging'),

]