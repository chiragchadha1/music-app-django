from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Artist, Playlist, Song, Like
from .forms import PlaylistForm


def home(request):
    songs = Song.objects.all()
    artists = Artist.objects.all()

    if request.user.is_authenticated:
        # Convert QuerySet to a list
        playlists = list(
            Playlist.objects.filter(creator=request.user).exclude(name="Liked Songs")
        )
        liked_song_ids = set(request.user.like_set.values_list("song_id", flat=True))

        # Check if "Liked Songs" playlist exists and insert it at the beginning
        liked_songs_playlist = Playlist.objects.filter(
            creator=request.user, name="Liked Songs"
        ).first()
        if liked_songs_playlist:
            playlists.insert(0, liked_songs_playlist)
    else:
        playlists = None
        liked_song_ids = None

    context = {
        "songs": songs,
        "artists": artists,
        "playlists": playlists,
        "liked_song_ids": liked_song_ids,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


# User Registration
def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("main:register")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        user.save()
        login(request, user)
        return redirect(
            "main:home"
        )  # Redirect to a home page or another appropriate page

    return render(request, "register.html")  # Path to your registration template


# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                "main:home"
            )  # Redirect to a home page or another appropriate page
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")  # Path to your login template


def logout_view(request):
    logout(request)
    return redirect("main:home")


def show_single_artist(request, artistID):
    artistObject = Artist.objects.get(id=artistID)
    songsList = artistObject.song_set.all()
    followers_count = artistObject.followers.count()  # Count the followers
    context = {
        "list_of_songs": songsList,
        "artist_name": artistObject.name,
        "followers": followers_count,  # Pass the count instead of the queryset
        "artist": artistObject,  # Pass the artist object to the template
    }
    return render(request, "artist.html", context)


@login_required
def liked_songs(request):
    playlist = Playlist.objects.get(creator=request.user, name="Liked Songs")
    liked_song_ids = set(request.user.like_set.values_list("song_id", flat=True))

    return render(
        request,
        "liked_songs.html",
        {"playlist": playlist, "liked_song_ids": liked_song_ids},
    )


@login_required
def show_single_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
    songs_in_playlist = playlist.songs.all()
    all_songs = Song.objects.all()
    filtered_songs = all_songs.exclude(
        id__in=songs_in_playlist.values_list("id", flat=True)
    )
    liked_song_ids = set(request.user.like_set.values_list("song_id", flat=True))

    if request.method == "POST":
        song_id = request.POST.get("song_id")
        song = get_object_or_404(Song, id=song_id)
        if "add_song" in request.POST:
            playlist.songs.add(song)
        elif "remove_song" in request.POST:
            playlist.songs.remove(song)
        return redirect(
            "main:show_single_playlist", playlist_id=playlist_id
        )  # Redirect to refresh the page

    context = {
        "playlist": playlist,
        "songs_in_playlist": songs_in_playlist,
        "filtered_songs": filtered_songs,
        "liked_song_ids": liked_song_ids,
    }
    return render(request, "playlist.html", context)


@login_required
def like_unlike_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    like, created = Like.objects.get_or_create(user=request.user, song=song)

    if not created:
        like.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("main:home")))


@login_required
def create_playlist(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            new_playlist = form.save(commit=False)
            new_playlist.creator = request.user
            new_playlist.save()
            messages.success(request, "Playlist created successfully.")
            return redirect("main:home")  # Or redirect to the new playlist's page
    else:
        form = PlaylistForm()

    return render(request, "create_playlist.html", {"form": form})


@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
    playlist.delete()
    messages.success(request, "Playlist deleted successfully.")
    return redirect("main:home")
