from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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
