from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from mypage.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)