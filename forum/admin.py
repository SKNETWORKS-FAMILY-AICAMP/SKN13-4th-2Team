from django.contrib import admin
from .models import PlaylistPost, Comment

@admin.register(PlaylistPost)
class PlaylistPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'playlist', 'created_at', 'total_likes')
    search_fields = ('title', 'author__username', 'playlist__name')
    list_filter = ('created_at', 'author')
    raw_id_fields = ('author', 'playlist', 'likes')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')
    list_filter = ('created_at', 'author')
    raw_id_fields = ('post', 'author')
