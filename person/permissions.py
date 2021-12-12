from serious_django_permissions.permissions import Permission

from person.models import Person


class CanCreatePersonPermission(Permission):
    model = Person
    description = "can create person"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanCreatePersonPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanUpdatePersonPermission(Permission):
    model = Person
    description = "can update person"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanUpdatePersonPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True
