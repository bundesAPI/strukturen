from django.contrib import admin

from orgcharts.models import OrgChartURL, OrgChart, OrgChartError

from reversion.admin import VersionAdmin


@admin.register(OrgChartURL)
class OrgChartURLAdmin(VersionAdmin):
    autocomplete_fields = ["organisation_entity"]
    search_fields = ["organisation_entity"]


@admin.register(OrgChart)
class OrgChartAdmin(VersionAdmin):
    pass


@admin.register(OrgChartError)
class OrgChartErrorAdmin(VersionAdmin):
    pass
