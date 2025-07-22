from django.db import models
from django.conf import settings
from mypage.models import Playlist

class PlaylistPost(models.Model):
    """
    사용자가 자신의 플레이리스트를 자랑하는 게시물 모델
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlist_posts')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='shared_posts')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, help_text="플레이리스트에 대한 간단한 소개를 적어주세요.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_playlist_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"'{self.playlist.name}' by {self.author.username}"

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    """
    플레이리스트 게시물에 대한 댓글 모델
    """
    post = models.ForeignKey(PlaylistPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlist_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
