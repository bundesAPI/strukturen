import reversion
from django.db import models
from claims.models import Entity

@reversion.register()
class OrganisationEntity(Entity):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('OrganisationEntity', null=True, blank=True, on_delete=models.SET_NULL, related_name="children")

    def __str__(self):
        if not self.parent:
            return self.name
        else:
            return f"{self.name} - {self.parent}"