from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/edit/', views.edit_playlist, name='edit_playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('history/', views.listening_history, name='listening_history'),
]
