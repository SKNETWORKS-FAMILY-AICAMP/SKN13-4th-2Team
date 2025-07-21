from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import EmailChangeForm, SignupForm

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:index')  # 회원가입 성공 후 홈페이지로 리다이렉트
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:email_change_done')
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, 'accounts/email_change_form.html', {'form': form})

@login_required
def email_change_done(request):
    return render(request, 'accounts/email_change_done.html')
