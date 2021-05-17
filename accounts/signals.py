from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def owner_profile(sender, instance, created, **kwargs):
    if created:
        pin = getattr(instance, 'pin', randint(1111, 9999))  # nosec
        Profile.objects.create(**{
            'name': instance.name, 'pin': pin, 'user': instance,
            'role': Profile.ROLE.owner
        })
