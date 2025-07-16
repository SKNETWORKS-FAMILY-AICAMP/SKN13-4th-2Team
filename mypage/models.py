from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    song_title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-listened_at']
        verbose_name_plural = "Listening Histories"

    def __str__(self):
        return f'{self.song_title} by {self.artist} ({self.user.username})'
