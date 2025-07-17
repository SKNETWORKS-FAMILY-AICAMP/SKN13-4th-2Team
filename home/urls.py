from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('music_player_popup/', views.music_player_popup, name='music_player_popup'),
]