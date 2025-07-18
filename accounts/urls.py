from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', success_url=reverse_lazy('mypage:index')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # allauth의 URL 추가


    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Password change views
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),

    # Email change views
    path('email_change/', views.email_change, name='email_change'),
    path('email_change/done/', views.email_change_done, name='email_change_done'),



]