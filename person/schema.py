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
from person.permissions import CanCreatePersonPermission, CanUpdatePersonPermission
from person.services import PersonService


class CreatePerson(FailableMutation):
    person = graphene.Field(PersonNode)

    class Arguments:
        name = graphene.String(required=True)
        position = graphene.String(required=False)

    @permissions_checker([IsAuthenticated, CanCreatePersonPermission])
    def mutate(self, info, name, position):
        user = get_user_from_info(info)
        try:
            result = PersonService.create_person(user, name, position)
        except PersonService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreatePerson(success=True, person=result)


class UpdatePerson(FailableMutation):
    person = graphene.Field(PersonNode)

    class Arguments:
        person_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        position = graphene.String(required=False)

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
                position=position,
            )
        except PersonService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdatePerson(success=True, person=result)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()


## Schema
schema = graphene.Schema(mutation=Mutation)
