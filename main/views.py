from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse

from .models import Artist, Playlist, Song, Like

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

def show_playlists(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
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