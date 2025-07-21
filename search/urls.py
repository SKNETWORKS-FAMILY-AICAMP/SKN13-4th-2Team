from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify_search/', views.spotify_search, name='spotify_search'),
]
