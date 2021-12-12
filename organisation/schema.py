import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphql_relay import from_global_id
from serious_django_graphene import FailableMutation, get_user_from_info, MutationExecutionException
from serious_django_services import NotPassed

from claims.schema import OrganisationEntityNode
from organisation.permissions import CanCreateOrganisationEntityPermission, CanUpdateOrganisationEntityPermission
from organisation.services import OrganisationEntityService



class CreateOrganisationEntity(FailableMutation):
    organisation_entity = graphene.Field(OrganisationEntityNode)

    class Arguments:
        name = graphene.String(required=True)
        short_name = graphene.String(required=False)
        parent_id = graphene.ID(required=False)

    @permissions_checker([IsAuthenticated, CanCreateOrganisationEntityPermission])
    def mutate(self, info, name, short_name=NotPassed, parent_id=NotPassed):
        user = get_user_from_info(info)
        if parent_id != NotPassed:
            parent_id = int(from_global_id(parent_id)[1])
        try:
            result = OrganisationEntityService.create_organisation_entity(user,
                                                                          name=name,
                                                                          short_name=short_name,
                                                                          parent_id=parent_id)
        except OrganisationEntityService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrganisationEntity(success=True, organisation_entity=result)




class UpdateOrganisationEntity(FailableMutation):
    organisation_entity = graphene.Field(OrganisationEntityNode)

    class Arguments:
        organisation_entity_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        short_name = graphene.String(required=False)
        parent_id = graphene.ID(required=False)

    @permissions_checker([IsAuthenticated, CanUpdateOrganisationEntityPermission])
    def mutate(
        self,
        info,
        organisation_entity_id,
        name=NotPassed,
        short_name=NotPassed,
        parent_id=NotPassed,
    ):
        user = get_user_from_info(info)
        if parent_id != NotPassed:
            parent_id = int(from_global_id(parent_id)[1])
        try:
            result = OrganisationEntityService.update_organisation_entity(
                user,
                int(from_global_id(organisation_entity_id)[1]),
                name=name,
                short_name=short_name,
                parent_id=parent_id,
            )
        except OrganisationEntityService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdateOrganisationEntity(success=True, organisation_entity=result)


class Mutation(graphene.ObjectType):
    create_organisation_entity = CreateOrganisationEntity.Field()
    update_organisation_entity = UpdateOrganisationEntity.Field()

## Schema
schema = graphene.Schema( mutation=Mutation)

