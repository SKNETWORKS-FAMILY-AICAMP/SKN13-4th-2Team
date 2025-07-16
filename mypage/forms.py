from django import forms
from .models import Profile, Playlist

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description']