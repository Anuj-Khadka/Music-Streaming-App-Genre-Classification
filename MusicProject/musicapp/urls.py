from django.urls import path
from . import views

# Add URLConf
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('mymusic/', views.mymusic, name='mymusic'),
    path('classify/', views.classify, name='classify'),
    path('result/', views.model_form_upload, name='result'),
    path('music/<int:id>/',views.PlaylistClassify, name="music"),
    path('playlist/', views.playlist, name='playlist'),
    path('recommend/', views.recommend, name='recommend'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('about',views.about, name = 'about'),
    path('recent/', views.recent, name='recent'),
    path('nepali_songs/', views.nepali_songs, name='nepali_songs'),
    path('hindi_songs/', views.hindi_songs, name='hindi_songs'),
    path('english_songs/', views.english_songs, name='english_songs'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),

    

]
