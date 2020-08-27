from .views import Reparse, Gkh, House, GetListOfStreets, IgnoreList, FavList, WatchList, GetIgnore, GetFav, GetWatch, \
    HouseListView, CreateClientSet, GetClientSet, CreatePhotoArhive, HouseClient
from django.urls import path, include
from domofound2.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('reparse/', Reparse.as_view()),
    path('get_base/<int:page_size>', HouseListView.as_view()),
    path('ignore/', IgnoreList.as_view()),
    path('get_ignore/', GetIgnore.as_view()),
    path('get_fav/', GetFav.as_view()),
    path('get_list_streets/', GetListOfStreets.as_view()),
    path('get_watch/', GetWatch.as_view()),
    path('fav/', FavList.as_view()),
    path('watch/', WatchList.as_view()),
    path('get_house/<int:pk>', House.as_view()),
    path('get_house_client/<int:pk>', HouseClient.as_view()),
    path('get_jkh/<int:pk>', Gkh.as_view()),
    path('create_user_set/', CreateClientSet.as_view()),
    path('get_user_set/', GetClientSet.as_view()),
    path('get_archive/<int:pk>', CreatePhotoArhive.as_view())
]