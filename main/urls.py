from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('playlists/liked_songs/', views.liked_songs, name='liked_songs'),

    path("artist/<int:artistID>", views.show_single_artist, name="show_single_artist"),
    path('playlist/<int:playlist_id>/', views.show_single_playlist, name='show_single_playlist'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/delete/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
    path('song/<int:song_id>/like_unlike/', views.like_unlike_song, name='like_unlike_song'),
]
