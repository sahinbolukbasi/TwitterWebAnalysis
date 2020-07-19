from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns=[
    path('hastagtweet/<hastag>',FilterTweet, name='hastagtweet'),
    path('delete/<int:id>',ClearContact, name='clearcontact'),
    path('',IndexView,name='index'),
    path('analizler/',AnalizView, name='analizler'),
    path('contact/',ContactView, name='contact'),
    path('tweets/',TweetView, name='tweets'),  
    path('tweetsgetir/',TweetGetir, name='tweetsgetir'), 
    path('analizistek/',AnalizIstekView, name='analizistek'), 
    path('hesap/',HesapView, name='hesap'), 

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)