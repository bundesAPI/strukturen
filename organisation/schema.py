import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from serious_django_graphene import (
    FailableMutation,
    get_user_from_info,
    MutationExecutionException,
)
from serious_django_services import NotPassed

from claims.schema import OrganisationEntityNode
from organisation.models import OrganisationAddress
from organisation.permissions import (
    CanCreateOrganisationEntityPermission,
    CanUpdateOrganisationEntityPermission,
)
from organisation.services import OrganisationEntityService, OrganisationAddressService


class OrganisationAddressNode(DjangoObjectType):
    class Meta:
        model = OrganisationAddress
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CreateOrganisationEntity(FailableMutation):
    organisation_entity = graphene.Field(OrganisationEntityNode)

    class Arguments:
        name = graphene.String(required=True)
        short_name = graphene.String(required=False)
        parent_id = graphene.ID(required=False)
        locations = graphene.List(graphene.ID)

    @permissions_checker([IsAuthenticated, CanCreateOrganisationEntityPermission])
    def mutate(
        self, info, name, short_name=NotPassed, locations=[], parent_id=NotPassed
    ):
        user = get_user_from_info(info)
        if parent_id != NotPassed:
            parent_id = int(from_global_id(parent_id)[1])

        if locations != NotPassed:
            locations = [int(from_global_id(l)[1]) for l in locations]
        try:
            result = OrganisationEntityService.create_organisation_entity(
                user,
                name=name,
                short_name=short_name,
                locations=locations,
                parent_id=parent_id,
            )
        except OrganisationEntityService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrganisationEntity(success=True, organisation_entity=result)


class UpdateOrganisationEntity(FailableMutation):
    organisation_entity = graphene.Field(OrganisationEntityNode)

    class Arguments:
        organisation_entity_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        short_name = graphene.String(required=False)
        locations = graphene.List(graphene.ID)
        parent_id = graphene.ID(required=False)

    @permissions_checker([IsAuthenticated, CanUpdateOrganisationEntityPermission])
    def mutate(
        self,
        info,
        organisation_entity_id,
        name=NotPassed,
        locations=NotPassed,
        short_name=NotPassed,
        parent_id=NotPassed,
    ):
        user = get_user_from_info(info)
        if parent_id != NotPassed:
            parent_id = int(from_global_id(parent_id)[1])
        if locations != NotPassed:
            locations = [int(from_global_id(l)[1]) for l in locations]
        try:
            result = OrganisationEntityService.update_organisation_entity(
                user,
                int(from_global_id(organisation_entity_id)[1]),
                name=name,
                short_name=short_name,
                locations=locations,
                parent_id=parent_id,
            )
        except OrganisationEntityService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdateOrganisationEntity(success=True, organisation_entity=result)


class CreateOrganisationAddress(FailableMutation):
    organisation_address = graphene.Field(OrganisationAddressNode)

    class Arguments:
        name = graphene.String(required=True)
        street = graphene.String(required=False)
        city = graphene.String(required=True)
        postal_code = graphene.String(required=True)
        country = graphene.String(required=True)
        phone_prefix = graphene.String(required=True)

    @permissions_checker([IsAuthenticated, CanCreateOrganisationEntityPermission])
    def mutate(self, info, name, street, city, postal_code, country, phone_prefix):
        user = get_user_from_info(info)

        try:
            result = OrganisationAddressService.create_address(
                user,
                name=name,
                street=street,
                city=city,
                postal_code=postal_code,
                country=country,
                phone_prefix=phone_prefix,
            )
        except OrganisationAddressService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrganisationAddress(success=True, organisation_address=result)


class UpdateOrganisationAddress(FailableMutation):
    organisation_address = graphene.Field(OrganisationAddressNode)

    class Arguments:
        organisation_address_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        street = graphene.String(required=False)
        city = graphene.String(required=False)
        postal_code = graphene.String(required=False)
        country = graphene.String(required=False)
        phone_prefix = graphene.String(required=False)

    @permissions_checker([IsAuthenticated, CanUpdateOrganisationEntityPermission])
    def mutate(
        self,
        info,
        organisation_address_id,
        name=NotPassed,
        street=NotPassed,
        city=NotPassed,
        postal_code=NotPassed,
        phone_prefix=NotPassed,
        country=NotPassed,
    ):
        user = get_user_from_info(info)
        try:
            result = OrganisationAddressService.update_address(
                user,
                int(from_global_id(organisation_address_id)[1]),
                name=name,
                street=street,
                city=city,
                postal_code=postal_code,
                phone_prefix=phone_prefix,
                country=country,
            )
        except OrganisationAddressService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdateOrganisationEntity(success=True, organisation_address=result)


class Mutation(graphene.ObjectType):
    create_organisation_entity = CreateOrganisationEntity.Field()
    update_organisation_entity = UpdateOrganisationEntity.Field()
    create_organisation_address = CreateOrganisationAddress.Field()
    update_organisation_address = UpdateOrganisationAddress.Field()


class Query(graphene.ObjectType):
    organisation_address = relay.Node.Field(OrganisationAddressNode)
    all_organisation_addresses = DjangoFilterConnectionField(OrganisationAddressNode)


## Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
