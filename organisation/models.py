import reversion
from django.db import models
from claims.models import Entity


@reversion.register()
class OrganisationAddress(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5, blank=True)
    country = models.CharField(max_length=2)
    phone_prefix = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name


@reversion.register()
class OrganisationEntity(Entity):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        "OrganisationEntity",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    locations = models.ManyToManyField(
        OrganisationAddress, related_name="organisations", blank=True
    )

    def __str__(self):
        if not self.parent:
            return self.name
        else:
            return f"{self.name} - {self.parent}"
