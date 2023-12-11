from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Artist(models.Model):

    name=models.CharField(max_length=30)
    followers=models.ManyToManyField(User)

    def __str__(self):

        string=f"{self.name}"
        return string

class Song(models.Model):

    title=models.CharField(max_length=30)
    duration=models.DurationField()
    language=models.CharField(max_length=5)
    releaseDate=models.DateField()
    album=models.CharField(max_length=30)
    artists=models.ManyToManyField(Artist)

    def __str__(self):

        string=f"{self.title}"
        return string
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

class Playlist(models.Model):

    name=models.CharField(max_length=20)
    duration = models.IntegerField(blank=True, null=True)
    songs=models.ManyToManyField(Song)
    creator=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        string=f"{self.name}"
        return string

class LikedSong(models.Model):
    #user: FK - each liked song is associated with one User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #song: FK - each liked song is associated with one song
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    
    