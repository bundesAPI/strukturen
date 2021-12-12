import reversion
from django.db import models
from claims.models import Entity


@reversion.register()
class Person(Entity):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
