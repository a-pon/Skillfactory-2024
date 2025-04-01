from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('adverts/<int:pk>/', AdvertDetail.as_view(), name='advert_detail'),
    path('adverts/create/', AdvertCreate.as_view(), name='advert_create'),
    path('adverts/<int:pk>/edit/', AdvertUpdate.as_view(), name='advert_edit'),
    # path('adverts/<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
    path('adverts/<int:pk>/respond/', RespondCreate.as_view(), name='respond_create'),
    path('responds/', RespondList.as_view(), name='respond_list'),
    path('responds/<int:pk>/', RespondDetail.as_view(), name='respond_detail'),
    path('responds/<int:pk>/accept/', accept_respond, name='accept_respond'),
    path('responds/<int:pk>/delete/', delete_respond, name='delete_respond'),
]
