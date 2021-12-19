import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import relay, Connection, Union
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from serious_django_graphene import (
    FailableMutation,
    get_user_from_info,
    MutationExecutionException,
)

from claims.models import (
    ValueClaim,
    RelationshipClaim,
    Claim,
    Entity,
    ClaimType,
    ClaimSource,
)
from claims.permissions import CanCreateValueClaimPermission
from claims.services import ValueClaimService, ClaimService, RelationshipClaimService
from organisation.models import OrganisationEntity
from person.models import Person


class ClaimSourceNode(DjangoObjectType):
    class Meta:
        model = ClaimSource
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class ClaimTypeType(DjangoObjectType):
    class Meta:
        model = ClaimType
        filter_fields = ["id"]
        connection_class = Connection
        interfaces = (relay.Node,)


class ClaimTypeInterface(graphene.Interface):
    created_at = graphene.DateTime(required=True)
    source = graphene.List(ClaimSourceNode)
    claim_type = graphene.Field(ClaimTypeType)

    class Meta:
        interfaces = (relay.Node,)


class ValueClaimType(DjangoObjectType):
    class Meta:
        model = ValueClaim
        filter_fields = ["id"]
        connection_class = Connection
        interfaces = (relay.Node, ClaimTypeInterface)


class RelationshipClaimType(DjangoObjectType):
    target = graphene.Field(lambda: EntityUnion)
    entity = graphene.Field(lambda: EntityUnion)

    def resolve_target(root, info):
        print(root)
        return root.target

    class Meta:
        model = RelationshipClaim
        filter_fields = ["id"]
        connection_class = Connection
        interfaces = (relay.Node, ClaimTypeInterface)


class ClaimUnion(Union):
    class Meta:
        types = (ValueClaimType, RelationshipClaimType)


class ClaimConnection(graphene.Connection):
    class Meta:
        node = ClaimUnion


class EntityTypeInterface(graphene.Interface):
    claims = graphene.ConnectionField(ClaimConnection)
    reverse_claims = graphene.ConnectionField(ClaimConnection)
    created_at = graphene.DateTime(required=True)

    def resolve_claims(root, info):
        return root.claims.all()

    def resolve_reverse_claims(root, info):
        return root.reverse_claims.all()

    class Meta:
        model = Entity
        interfaces = (relay.Node,)


class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        filter_fields = ["id"]
        interfaces = (
            relay.Node,
            EntityTypeInterface,
        )


class OrganisationEntityNode(DjangoObjectType):
    class Meta:
        model = OrganisationEntity
        filter_fields = ["id"]
        interfaces = (
            relay.Node,
            EntityTypeInterface,
        )


class EntityUnion(Union):
    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Person):
            return PersonNode
        if isinstance(instance, OrganisationEntity):
            return OrganisationEntityNode

    class Meta:
        types = (
            PersonNode,
            OrganisationEntityNode,
        )


class EntityConnection(graphene.Connection):
    class Meta:
        node = EntityUnion


class CreateValueClaim(FailableMutation):
    value_claim = graphene.Field(ValueClaimType)

    class Arguments:
        value = graphene.JSONString(required=True)
        entity_id = graphene.ID(required=True)
        claim_type_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateValueClaimPermission])
    def mutate(self, info, value, entity_id, claim_type_id):
        user = get_user_from_info(info)
        try:
            result = ValueClaimService.create_value_claim(
                user,
                entity_id=int(from_global_id(entity_id)[1]),
                claim_type_id=int(from_global_id(claim_type_id)[1]),
                value=value,
            )
        except ValueClaimService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateValueClaim(success=True, value_claim=result)


class CreateRelationshipClaim(FailableMutation):
    relationship_claim = graphene.Field(RelationshipClaimType)

    class Arguments:
        value = graphene.JSONString(required=True)
        entity_id = graphene.ID(required=True)
        target_id = graphene.ID(required=True)
        claim_type_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateValueClaimPermission])
    def mutate(self, info, value, entity_id, target_id, claim_type_id):
        user = get_user_from_info(info)
        try:
            result = RelationshipClaimService.create_relationship_claim(
                user,
                entity_id=int(from_global_id(entity_id)[1]),
                target_id=int(from_global_id(target_id)[1]),
                claim_type_id=int(from_global_id(claim_type_id)[1]),
                value=value,
            )
        except RelationshipClaimService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateRelationshipClaim(success=True, relationship_claim=result)


class UpdateClaim(FailableMutation):
    claim = graphene.Field(ClaimUnion)

    class Arguments:
        value = graphene.JSONString(required=True)
        claim_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateValueClaimPermission])
    def mutate(self, info, claim_id, value):
        user = get_user_from_info(info)
        try:
            result = ClaimService.update_claim(
                user, claim_id=int(from_global_id(claim_id)[1]), value=value
            )
        except ClaimService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdateClaim(success=True, claim=result)


class Query(graphene.ObjectType):
    claims = graphene.ConnectionField(ClaimConnection)
    person = relay.Node.Field(PersonNode)
    organisation_entity = relay.Node.Field(OrganisationEntityNode)
    all_organisation_entities = DjangoFilterConnectionField(OrganisationEntityNode)
    claim_source = relay.Node.Field(ClaimSourceNode)
    all_people = DjangoFilterConnectionField(PersonNode)
    all_claim_types = DjangoFilterConnectionField(ClaimTypeType)

    def resolve_claims(self, info):
        return Claim.objects.all()


class Mutation(graphene.ObjectType):
    create_value_claim = CreateValueClaim.Field()
    create_relationship_claim = CreateRelationshipClaim.Field()
    update_claim = UpdateClaim.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
