from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from account.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def save_or_update_profile(sender, instance, **kwargs):
    Profile.objects.update_or_create(user=instance)
    instance.profile.save()


