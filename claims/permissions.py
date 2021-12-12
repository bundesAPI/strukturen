from serious_django_permissions.permissions import Permission

from claims.models import ValueClaim, RelationshipClaim


class CanCreateValueClaimPermission(Permission):
    model = ValueClaim
    description = "can create ValueClaim"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanCreateValueClaimPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True


class CanUpdateValueClaimPermission(Permission):
    model = ValueClaim
    description = "can update ValueClaim"

    @staticmethod
    def has_permission(context):
        return context.user.has_perm(CanUpdateValueClaimPermission)

    @staticmethod
    def has_object_permission(context, obj):
        return True
