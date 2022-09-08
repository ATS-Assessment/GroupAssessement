from .models import UserProfile, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()
    else:
        try:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.save()
        except:
            UserProfile.objects.create(user=instance)
