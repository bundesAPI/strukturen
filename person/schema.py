import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import relay, Connection
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from serious_django_graphene import (
    FailableMutation,
    get_user_from_info,
    MutationExecutionException,
)
from serious_django_services import NotPassed

from claims.schema import PersonNode
from person.models import PositionAbbreviation, PersonPosition
from person.permissions import CanCreatePersonPermission, CanUpdatePersonPermission
from person.services import PersonService


class PositionAbbreviationNode(DjangoObjectType):
    class Meta:
        model = PositionAbbreviation
        filter_fields = ["id", "name"]
        interfaces = (relay.Node,)


class PersonPositionNode(DjangoObjectType):
    class Meta:
        model = PersonPosition
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CreatePerson(FailableMutation):
    person = graphene.Field(PersonNode)

    class Arguments:
        name = graphene.String(required=True)
        position = graphene.ID(required=False)

    @permissions_checker([IsAuthenticated, CanCreatePersonPermission])
    def mutate(self, info, name, position):
        user = get_user_from_info(info)
        try:
            result = PersonService.create_person(
                user, name, int(from_global_id(position)[1])
            )
        except PersonService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreatePerson(success=True, person=result)


class UpdatePerson(FailableMutation):
    person = graphene.Field(PersonNode)

    class Arguments:
        person_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        position = graphene.ID(required=False)

    @permissions_checker([IsAuthenticated, CanUpdatePersonPermission])
    def mutate(
        self,
        info,
        person_id,
        name=NotPassed,
        position=NotPassed,
    ):
        user = get_user_from_info(info)
        try:
            result = PersonService.update_person(
                user,
                int(from_global_id(person_id)[1]),
                name=name,
                position=int(from_global_id(position)[1]),
            )
        except PersonService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdatePerson(success=True, person=result)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()


class Query(graphene.ObjectType):
    position_abbreviation = relay.Node.Field(PositionAbbreviationNode)
    all_position_abbreviations = DjangoFilterConnectionField(PositionAbbreviationNode)


## Schema
schema = graphene.Schema(mutation=Mutation, query=Query)
