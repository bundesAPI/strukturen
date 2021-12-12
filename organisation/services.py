import reversion
from django.contrib.auth.models import AbstractUser
from serious_django_services import Service, NotPassed, CRUDMixin

from organisation.forms import UpdateOrganisationEntityForm, CreateOrganisationEntityForm
from organisation.models import OrganisationEntity
from organisation.permissions import CanCreateOrganisationEntityPermission, CanUpdateOrganisationEntityPermission


class OrganisationEntityServiceException(Exception):
    pass

class OrganisationEntityService(Service, CRUDMixin):
    update_form = UpdateOrganisationEntityForm
    create_form = CreateOrganisationEntityForm

    service_exceptions = ()
    model = OrganisationEntity


    @classmethod
    def retrieve_organisation_entity(cls, id: int) -> OrganisationEntity:
        """
        get an organisation_entity by id
        :param id: id of the organisation_entity
        :return: the organisation_entity object
        """
        try:
            org_entity = cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            raise OrganisationEntityServiceException(
                "OrganisationEntity not found."
            )

        return org_entity

    @classmethod
    def create_organisation_entity(cls, user: AbstractUser, name: str, short_name: str = NotPassed, parent_id: int = NotPassed) -> OrganisationEntity:
        """ create a new OrganisationEntity
            :param user: the user calling the service
            :name: -  full name of the entity "Bundesminsiterium für Bildung und Forschung
            :short_name: -  short_name "BMBF" (Optional)
            :parent_id: - id of the parent institution (Optional)
            :returns: the newly created organisation_entity instance
        """

        if not user.has_perm(CanCreateOrganisationEntityPermission):
            raise PermissionError("You are not allowed to create an OrganisationEntity.")

        with reversion.create_revision():
            person = cls._create({"name": name, "short_name": short_name, "parent": parent_id})
            reversion.set_user(user)

        return person

    @classmethod
    def update_organisation_entity(cls, user: AbstractUser, organisation_entity_id: int, name: str = NotPassed, short_name: str = NotPassed, parent_id: int = NotPassed) -> OrganisationEntity:
        """ create a new person
            :param user: the user calling the service
            :param organisation_entity_id: - ID of the exsisting entity that should be updated
            :param last_name: - Last name
            :param first_name: - First name (Optional)
            :return: the updated organisation_entity instance
        """

        organisation_entity = cls.retrieve_organisation_entity(organisation_entity_id)

        if not user.has_perm(CanUpdateOrganisationEntityPermission, organisation_entity):
            raise PermissionError("You are not allowed to update this OrganisationEntity.")

        with reversion.create_revision():
            organisation_entity = cls._update(
                organisation_entity_id,
                {
                    "name": name,
                    "short_name": short_name,
                    "parent": parent_id
                },
            )
            reversion.set_user(user)
            reversion.set_comment(f"update via service by {user}")

        organisation_entity.refresh_from_db()
        return organisation_entity