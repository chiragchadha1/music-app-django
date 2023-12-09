"""
URL configuration for musicproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views

app_name= "main"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('artists/', views.show_artists, name='artists'),
    path('playlists/', views.show_playlists, name='playlists'),
    path('songs/', views.show_songs, name='songs'),
    # path("show_playlist/<int:playlistID>", views.show_playlist, name="playlist"),
    # path("showPlaylist/addNew", views.addNewPlaylist, name="addNewPlaylist"),
    # path("like/<int:songID>", views.likesong, name="likesong"),
    path('song/<int:song_id>/like/', views.like_song, name='like_song'),
]
