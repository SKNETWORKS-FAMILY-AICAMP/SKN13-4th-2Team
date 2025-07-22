from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import EmailChangeForm, SignupForm
from django.contrib.auth import logout
from django.core.exceptions import ValidationError  # 추가
from django.utils.http import url_has_allowed_host_and_scheme

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # 수정된 부분
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('home:index')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = SignupForm()
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/signup.html', {'form': form, 'next': next_url})



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



@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home:index')
    return render(request, 'accounts/delete_account_confirm.html')


# 이메일의 domain과 site_name을 수정하기 위한 커스텀 뷰
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": {'site_name': 'SKN13-4th-2Team'}, # 사이트 이름 수정
        }
        # 현재 요청에서 실제 호스트(도메인)를 가져와 사용
        form.save(domain_override=self.request.get_host(), **opts)
        return redirect(self.get_success_url())

