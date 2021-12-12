from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from oauth.models import UserProfile
