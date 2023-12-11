from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Artist, Playlist, Song, Like, LikedSong

from .forms import SongForm
from .forms import PlaylistForm


def home(request):
    songs = Song.objects.all()
    artists = Artist.objects.all()
    playlists = Playlist.objects.all()
    context = {
        'songs': songs,
        'artists': artists,
        'playlists': playlists
    }
    return render(request, 'home.html', context)

# User Registration
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('main:register')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        user.save()
        login(request, user)
        return redirect('main:home')  # Redirect to a home page or another appropriate page

    return render(request, 'register.html')  # Path to your registration template

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')  # Redirect to a home page or another appropriate page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')  # Path to your login template

def logout_view(request):
    logout(request)
    return redirect('main:home')

def show_artists(request):
    artists = Artist.objects.all()
    context = {'artists': artists}
    return render(request, 'artists.html', context)

def playlists(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, 'playlists.html', context)

def show_playlists(request, playlistID):
    playlistObj = Playlist.objects.get(id=playlistID)
    # i don't think this line is right
    playlistList = Playlist.playlists_set.all()
    context = {"list_of_playlists" : playlistList, "playlists_Name" : playlistObj.name}
    return render(request, 'playlists.html', context)

def show_songs(request):
    songs = Song.objects.all()
    context = {'songs': songs}
    return render(request, 'songs.html', context)

def chooseArtist(request, artistID):

    artistObject = Artist.objects.get(id = artistID)

    songsList = artistObject.song_set.all()

    context ={"list_of_songs": songsList, "artist_name": artistObject.name, "followers": artistObject.followers}

    return render(request, "showArtist.html", context)



def like_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    # Assuming the user is logged in and authenticated
    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(user=request.user, song=song)
        if not created:
            like.delete()
        return JsonResponse({'liked': created})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

def about(request):
    return render(request, 'about.html')


# like/dislike song function
def like_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song_id = form.cleaned_data['song_id']
            action = form.cleaned_data['action']
            try:
                song = Song.objects.get(pk=song_id)
                if action == 'like':
                    LikedSong.objects.create(user=request.user, song=song)
                elif action == 'dislike':
                    liked_song = LikedSong.objects.filter(user=request.user, song=song).first()
                    if liked_song:
                        liked_song.delete()
                return redirect('show_songs', song.id)
            except Song.DoesNotExist:
                return render(request, 'songs.html', {'form': form, 'error_message': 'Song does not exist'})
    else:
        form = SongForm()
    return render(request, 'songs.html', {'form': form})

# liked songs playlist
'''
@login_required
def view_liked_songs(request):
    liked_songs = LikedSong.objects.filter(user=request.user)

    # should be placed in playlist.html ?
    return render(request, 'playlists.html', {'liked_songs': liked_songs})
'''
# create a playlist
'''
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('main:show_songs')
    else:
        form = PlaylistForm()
    return render(request, 'playlists.html', {'form': form})
'''
@login_required
def addNewPlaylist(request):

    if request.method != "POST":

        form = PlaylistForm()

    else:

        form = PlaylistForm(data=request.POST) # not meant to be filled, meant to be checked

        if form.is_valid():

            form.save() # stored in the db

            return redirect('main:playlists')

    context = {"form" : form} #executed if the form

    return render(request, "playlists.html", context)
# add songs to playlist
def add_song_to_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id)
    song = Song.objects.get(id=song_id)
    if song not in playlist.songs.all():
        playlist.songs.add(song)
    return redirect('show_playlists', playlist_id=playlist_id)

# delete songs from playlist
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id)
    song = Song.objects.get(id=song_id)
    playlist.songs.remove(song)
    return redirect('show_playlists', playlist_id=playlist_id)

