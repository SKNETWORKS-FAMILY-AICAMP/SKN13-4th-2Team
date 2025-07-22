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
    tracks = models.ManyToManyField('Track', related_name='playlists', blank=True) # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    track_url = models.URLField(max_length=500, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True) # 추가된 필드

    def __str__(self):
        return f"{self.title} - {self.artist}"

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='listening_records', null=True, blank=True)
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-listened_at']
        verbose_name_plural = "Listening Histories"

    def __str__(self):
        return f'{self.track.title} by {self.track.artist} ({self.user.username})'
