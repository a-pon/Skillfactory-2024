from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    DefaultView, ProfileView,
    PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, PostLimit,
    CategoryList, CategoryDetail,
    upgrade_me, subscribe_me
    )

urlpatterns = [
    path('', cache_page(60)(DefaultView.as_view())),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('news/', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/limit/', PostLimit.as_view(), name='post_limit'),
    path('articles/<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe/', subscribe_me, name='subscribe'),
]
