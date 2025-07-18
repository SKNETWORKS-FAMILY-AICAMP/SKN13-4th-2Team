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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control w-full px-4 py-2 rounded-lg border bg-[#191919] text-gray-100',
                'placeholder': '플레이리스트 이름'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-full px-4 py-2 rounded-lg border bg-[#191919] text-gray-100',
                'rows': 5,
                'style': 'resize: none;',
                'placeholder': '설명'
            }),
        }
