from django import forms
from .models import Profile, Playlist

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

class PlaylistForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '플레이리스트 이름'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'resize: none;', 'placeholder': '설명'}), required=False)

    class Meta:
        model = Playlist
        fields = ['name', 'description']