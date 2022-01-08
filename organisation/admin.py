from django.contrib import admin

from organisation.models import OrganisationAddress
from orgcharts.models import OrgChartURL, OrgChart, OrgChartError

from reversion.admin import VersionAdmin


@admin.register(OrganisationAddress)
class OrganisationAddressAdmin(VersionAdmin):
    pass
