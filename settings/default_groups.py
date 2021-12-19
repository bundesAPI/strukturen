from serious_django_permissions.groups import Group

from person.permissions import CanCreatePersonPermission, CanUpdatePersonPermission


class AdministrativeStaffGroup(Group):
    permissions = [
        CanCreatePersonPermission,
        CanUpdatePersonPermission,
    ]
