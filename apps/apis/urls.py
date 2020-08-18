from django.contrib import admin
from django.urls import path, include
from domofound2.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('base/', include('apps.base.urls')),
    path('auth/', include('apps.users.urls'))
]