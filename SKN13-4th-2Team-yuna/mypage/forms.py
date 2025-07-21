from django import forms
from django.contrib.auth.models import User # User 모델 임포트
from .models import Profile, Playlist
from django.utils.translation import gettext_lazy as _ # 번역을 위해 추가

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, label=_("Email")) # 이메일 필드 추가

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스(Profile)가 제공되면, 연결된 User의 이메일로 필드를 초기화
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        # 이메일 필드가 cleaned_data에 있으면 User 모델에 저장
        if 'email' in self.cleaned_data:
            user = profile.user
            user.email = self.cleaned_data['email']
            user.save()
        return profile

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
