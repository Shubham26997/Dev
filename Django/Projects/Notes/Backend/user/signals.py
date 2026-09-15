from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from user.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(pre_save, sender=Profile)
def add_phone_number(sender, instance, **kwargs):
    if not instance.phone_number:
        instance.phone_number = '7871232726'
