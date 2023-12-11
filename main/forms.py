from django import forms

from .models import Song

from .models import Playlist

# LIKING/DISLIKING SONG functionality
class SongForm(forms.ModelForm):
    song_id = forms.IntegerField(widget=forms.HiddenInput)
    action = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Song
        fields = ['song_id', 'action']
        
# Playlist Form
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'creator']
        # 'key/associated field': 'text output of what is shown to user'
        labels = {'name' : 'Playlist Name', 'creator' : 'Your Name'}