from django import forms
from .models import PlaylistPost, Comment
from mypage.models import Playlist

class PlaylistPostForm(forms.ModelForm):
    class Meta:
        model = PlaylistPost
        fields = ['playlist', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-[#444] bg-[#191919] text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-[#444] bg-[#191919] text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500', 'rows': 4}),
            'playlist': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-[#444] bg-[#191919] text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['playlist'].queryset = Playlist.objects.filter(user=user)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-[#444] bg-[#191919] text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500',
                'rows': 3,
                'placeholder': '댓글을 입력하세요...'
            }),
        }
        labels = {
            'content': ''
        }
