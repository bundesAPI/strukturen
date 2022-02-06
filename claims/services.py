import json

import reversion
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from jsonschema.exceptions import ValidationError

from serious_django_services import Service, CRUDMixin, NotPassed
from jsonschema import validate

from claims.forms import CreateValueClaimForm, UpdateValueClaimForm
from claims.models import Entity, ClaimType, ValueClaim, Claim, RelationshipClaim
from claims.permissions import CanCreateValueClaimPermission


class EntityServiceException(Exception):
    pass


class ClaimTypeServiceException(Exception):
    pass


class ClaimServiceException(Exception):
    pass


class EntityService(Service):
    service_exceptions = (EntityServiceException,)
    model = Entity

    @classmethod
    def resolve_entity(cls, entity_id: int):
        """
        get an entity by id
        :param entity_id: id of the organisation_entity
        :return: the entity object
        """
        try:
            entity = cls.model.objects.get(pk=entity_id)
        except cls.model.DoesNotExist:
            raise EntityServiceException("Entity not found.")

        return entity


class ClaimTypeService(Service):
    service_exceptions = (ClaimTypeServiceException,)
    model = ClaimType

    @classmethod
    def resolve_claim_type(cls, claim_type_id: int):
        """
        get an claim_type by id
        :param claim_type_id: id of the claim_type
        :return: the claim_type object
        """
        try:
            claim_type = cls.model.objects.get(pk=claim_type_id)
        except cls.model.DoesNotExist:
            raise ClaimTypeServiceException("ClaimType not found.")

        return claim_type

    @classmethod
    def resolve_claim_type_by_codename(cls, code_name: str):
        """
        get a claim type by its codename
        :param code_name:  name of the claim you want to query
        :return: the claim object
        """
        try:
            claim_type = cls.model.objects.get(code_name=code_name)
        except cls.model.DoesNotExist:
            raise ClaimServiceException("ClaimType not found.")

        return claim_type


class ClaimService(Service, CRUDMixin):
    model = ValueClaim
    create_form = CreateValueClaimForm
    update_form = UpdateValueClaimForm
    service_exceptions = (ValidationError, PermissionError, ClaimServiceException)

    @classmethod
    def resolve_claim(cls, claim_id: int):
        """
        get a claim by id
        :param claim_id: id of the claim_type
        :return: the claim object
        """
        try:
            claim = cls.model.objects.get(pk=claim_id)
        except cls.model.DoesNotExist:
            raise ClaimServiceException("Claim not found.")

        return claim

    @classmethod
    def update_claim(cls, user: AbstractUser, claim_id: int, value: str):
        """update a new value claim
        :param user: user calling the service
        :param claim_id: id of the claim that should be updated
        :param value: json value of the claim
        """
        claim = ClaimService.resolve_claim(claim_id)

        # is the value valid json?
        validate(instance=value, schema=claim.claim_type.value_schema)

        if not user.has_perm(CanCreateValueClaimPermission):
            raise PermissionError("You are not allowed to create a ValueClaim.")

        with reversion.create_revision():
            claim = cls._update(
                claim_id,
                {"value": value},
            )
            reversion.set_user(user)
        return claim


class ValueClaimService(Service, CRUDMixin):
    model = ValueClaim
    create_form = CreateValueClaimForm
    update_form = UpdateValueClaimForm
    service_exceptions = (ValidationError, PermissionError, ClaimServiceException)

    @classmethod
    def create_value_claim(
        cls, user: AbstractUser, entity_id: int, claim_type_id: int, value: dict
    ):
        """create a new value claim
        :param user: user calling the service
        :param entity_id: entity id this claim is added to
        :param claim_type_id: claim type
        :param value: json value of the claim as dict
        """
        entity = EntityService.resolve_entity(entity_id)
        claim_type = ClaimTypeService.resolve_claim_type(claim_type_id)

        # is this claim type allowed for this entity type?
        if (
            ContentType.objects.get_for_model(entity)
            not in claim_type.content_type.all()
        ):
            raise ClaimServiceException(
                f"Entity Type {ContentType.objects.get_for_model(entity)} is not "
                f"supported by claim '{claim_type.name}'"
                f"(supported: {', '.join([c.name for c in claim_type.content_type.all()])})"
            )
        # is the value valid json?
        validate(instance=value, schema=claim_type.value_schema)

        if not user.has_perm(CanCreateValueClaimPermission):
            raise PermissionError("You are not allowed to create a ValueClaim.")

        with reversion.create_revision():
            value_claim = cls.model.objects.create(
                value=value, entity=entity, claim_type=claim_type
            )
            reversion.set_user(user)
        return value_claim


class RelationshipClaimService(Service, CRUDMixin):
    model = RelationshipClaim
    create_form = CreateValueClaimForm
    update_form = UpdateValueClaimForm
    service_exceptions = (ValidationError, PermissionError, ClaimServiceException)

    @classmethod
    def create_relationship_claim(
        cls,
        user: AbstractUser,
        entity_id: int,
        claim_type_id: int,
        target_id: int,
        value: str = NotPassed,
    ) -> object:
        """create a new relationship claim
        :param user: user calling the service
        :param entity_id: entity id this claim is added to
        :param claim_type_id: claim type
        :param value: json value of the claim
        """
        entity = EntityService.resolve_entity(entity_id)
        target = EntityService.resolve_entity(target_id)
        claim_type = ClaimTypeService.resolve_claim_type(claim_type_id)

        # is this claim type allowed for this entity type?
        if (
            ContentType.objects.get_for_model(entity)
            not in claim_type.content_type.all()
        ):
            raise ClaimServiceException(
                f"Entity Type {ContentType.objects.get_for_model(entity)} is not "
                f"supported by claim '{claim_type.name}' "
                f"(supported: {', '.join([c.name for c in claim_type.content_type.all()])})"
            )

        # is this claim type allowed for this target type?
        if (
            ContentType.objects.get_for_model(target)
            not in claim_type.content_type.all()
        ):
            raise ClaimServiceException(
                f"Entity Type {ContentType.objects.get_for_model(target)} is not "
                f"supported by claim '{claim_type.name}' "
                f"(supported: {', '.join([c.name for c in claim_type.content_type.all()])})"
            )
        if claim_type.value_schema:
            # is the value valid json?
            validate(instance=value, schema=claim_type.value_schema)

        if not value:
            value = NotPassed
        print(value)
        if not claim_type.value_schema and value is not NotPassed:
            raise ClaimServiceException(
                "This claim dosen't support additional attributes"
            )

        if not user.has_perm(CanCreateValueClaimPermission):
            raise PermissionError("You are not allowed to create a ValueClaim.")

        with reversion.create_revision():
            if value is not NotPassed:
                relationship_claim = cls.model.objects.create(
                    value=value, entity=entity, target=target, claim_type=claim_type
                )
            else:
                relationship_claim = cls.model.objects.create(
                    entity=entity, target=target, claim_type=claim_type
                )
            reversion.set_user(user)
        return relationship_claim
