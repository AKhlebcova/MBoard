from django.urls import path
from board.views import *
from django.views.generic.base import RedirectView
# from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', RedirectView.as_view(url='/posts/')),
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:id>', PostDetail.as_view(), name='post_detail'),
    # path('news/search/', PostSearch.as_view(), name='search_post'),
    path('posts/create/', PostCreate.as_view(), name='create_post'),
    # path('news/create/', NewsCreate.as_view(), name='create_news'),
    # path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='update_article'),
    # path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='update_news'),
    # path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete_article'),
    # path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    # path('index/', IndexView.as_view(), name='user_index'),
    # path('upgrade/', upgrade_me, name='upgrade'),
    # path('news/category/<int:pk>', CategoryPostList.as_view(), name='posts_category'),
    # path('news/category/<int:pk>/subscriber', subscriber, name='subscriber'),
    # path('start/', start, name='start'),
    # # path('log/', log, name='logging'),

]