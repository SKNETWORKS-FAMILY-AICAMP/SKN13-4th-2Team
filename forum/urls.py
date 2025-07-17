from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/', views.post_list, name='post_list'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
]
