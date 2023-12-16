# downloader/forms.py
from django import forms

class PlaylistForm(forms.Form):
    playlist_url = forms.URLField(label='Playlist URL', max_length=200)
