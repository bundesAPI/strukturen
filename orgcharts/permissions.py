from serious_django_permissions.permissions import Permission

from orgcharts.models import OrgChartURL, OrgChart
from person.models import Person


class CanCreateOrgChartURLPermission(Permission):
    model = OrgChartURL
    description = "can create orgchart url entity"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanCreateOrgChartURLPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanImportOrgChartPermission(Permission):
    model = OrgChart
    description = "can import the data of an orgchart initially"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanImportOrgChartPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True
