from serious_django_permissions.permissions import Permission

from person.models import Person


class CanCreateOrganisationEntityPermission(Permission):
    model = Person
    description = "can create organisation entity"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanCreateOrganisationEntityPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanUpdateOrganisationEntityPermission(Permission):
    model = Person
    description = "can update organisation entity"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanUpdateOrganisationEntityPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanCreateOrganisationAddressPermission(Permission):
    model = Person
    description = "can create organisation address"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanCreateOrganisationAddressPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanUpdateOrganisationAddressPermission(Permission):
    model = Person
    description = "can create organisation address"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanUpdateOrganisationAddressPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True
