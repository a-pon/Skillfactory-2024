from django.urls import path
from .views import (
    PostsList, PostDetail, PostSearch, PostCreate, ArticleCreate, PostUpdate, PostDelete
)

urlpatterns = [
    path('news/', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
