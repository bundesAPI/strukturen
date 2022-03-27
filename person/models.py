import reversion
from django.db import models
from claims.models import Entity
from django.utils.translation import ugettext as _


@reversion.register()
class PersonPosition(models.Model):
    name = models.CharField(max_length=255)
    female_name = models.CharField(max_length=255, blank=True, null=True)
    gender_neutral_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Gender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    UNKOWN = "UNKOWN", _("Unknown")


@reversion.register()
class PositionAbbreviation(models.Model):
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    position = models.ForeignKey(
        PersonPosition, related_name="abbreviations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


@reversion.register()
class Person(Entity):
    name = models.CharField(max_length=255)
    position = models.ForeignKey(
        PositionAbbreviation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="persons",
    )

    def __str__(self):
        return self.name
