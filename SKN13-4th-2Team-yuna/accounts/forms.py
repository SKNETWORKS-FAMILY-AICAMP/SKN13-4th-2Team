from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from mypage.models import Profile

class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True, label=_("New Email"))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This email address is already in use."))
        return email

class SignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=100, required=True, label=_("Nickname"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('nickname',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, nickname=self.cleaned_data['nickname'])
        return user