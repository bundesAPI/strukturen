from django.db import models
from django.utils.translation import gettext_lazy as _
import reversion

from organisation.models import OrganisationEntity


class OrgChartStatusChoices(models.TextChoices):
    NEW = "NEW", _("new")
    PARSED = "PARSED", _("parsed")
    IMPORTED = "IMPORTED", _("imported")


class OrgChartErrorStatusChoices(models.TextChoices):
    NEW = "NEW", _("new")
    PARSED = "RESOLVED", _("resolved")


@reversion.register()
class OrgChartURL(models.Model):
    organisation_entity = models.ForeignKey(
        OrganisationEntity, on_delete=models.CASCADE, related_name="orgcharts"
    )
    created_at = models.DateTimeField(auto_created=True)
    url = models.URLField()

    def __str__(self):
        return f"{self.organisation_entity} - {self.url}"


@reversion.register()
class OrgChart(models.Model):
    org_chart_url = models.ForeignKey(
        OrgChartURL, on_delete=models.CASCADE, related_name="orgchart_documents"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    document_hash = models.CharField(max_length=255)
    document = models.FileField()
    raw_source = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrgChartStatusChoices.choices,
        default=OrgChartStatusChoices.NEW,
    )

    def __str__(self):
        return f"{self.org_chart_url} - {self.created_at}"

    class Meta:
        unique_together = [["org_chart_url", "document_hash"]]


@reversion.register()
class OrgChartError(models.Model):
    org_chart_url = models.ForeignKey(
        OrgChartURL, on_delete=models.CASCADE, related_name="errors"
    )
    message = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=OrgChartErrorStatusChoices.choices,
        default=OrgChartErrorStatusChoices.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
