from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext as _
from django.conf import settings


class UserProfile(models.Model):
    """
    represents user profile settings
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    profile_picture = models.ImageField(null=True, blank=True)
    profile_setup_done = models.BooleanField(default=False)
    language = models.CharField(
        default=settings.LANGUAGE_CODE, choices=settings.LANGUAGES, max_length=20
    )

    def __str__(self):
        return f"{self.user}: Profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
