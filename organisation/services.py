from typing import List

import reversion
from django.contrib.auth.models import AbstractUser
from serious_django_services import Service, NotPassed, CRUDMixin

from organisation.forms import UpdateOrganisationEntityForm, CreateOrganisationEntityForm, \
    UpdateOrganisationAddressForm, CreateOrganisationAddressForm
from organisation.models import OrganisationEntity, OrganisationAddress
from organisation.permissions import CanCreateOrganisationEntityPermission, CanUpdateOrganisationEntityPermission, \
    CanUpdateOrganisationAddressPermission, CanCreateOrganisationAddressPermission


class OrganisationEntityServiceException(Exception):
    pass


class OrganisationAddressServiceException(Exception):
    pass


class OrganisationEntityService(Service, CRUDMixin):
    update_form = UpdateOrganisationEntityForm
    create_form = CreateOrganisationEntityForm

    service_exceptions = (OrganisationEntityServiceException, )
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
    def create_organisation_entity(cls, user: AbstractUser, name: str, short_name: str = NotPassed,
                                   parent_id: int = NotPassed, locations: List[int]=NotPassed) -> OrganisationEntity:
        """ create a new OrganisationEntity
            :param user: the user calling the service
            :param name: -  full name of the entity "Bundesminsiterium für Bildung und Forschung
            :param short_name: -  short_name "BMBF" (Optional)
            :param parent_id: - id of the parent institution (Optional)
            :param locations: - list of location ids (Optional)
            :returns: the newly created organisation_entity instance
        """

        if not user.has_perm(CanCreateOrganisationEntityPermission):
            raise PermissionError("You are not allowed to create an OrganisationEntity.")

        with reversion.create_revision():
            person = cls._create({"name": name,
                                  "short_name": short_name,
                                  "parent": parent_id,
                                  "locations": locations
                                  })
            reversion.set_user(user)

        return person

    @classmethod
    def update_organisation_entity(cls, user: AbstractUser, organisation_entity_id: int, name: str = NotPassed,
                                   short_name: str = NotPassed, parent_id: int = NotPassed,
                                   locations: List[int] = NotPassed) -> OrganisationEntity:
        """ create a new person
            :param organisation_entity_id: - ID of the exsisting entity that should be updated
            :param user: the user calling the service
            :param name: -  full name of the entity "Bundesminsiterium für Bildung und Forschung
            :param short_name: -  short_name "BMBF" (Optional)
            :param parent_id: - id of the parent institution (Optional)
            :param locations: - list of location ids (Optional)
            :returns: the updated organisation_entity instance
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
                    "parent": parent_id,
                    "locations": locations
                },
            )
            reversion.set_user(user)
            reversion.set_comment(f"update via service by {user}")

        organisation_entity.refresh_from_db()
        return organisation_entity


class OrganisationAddressService(Service, CRUDMixin):
    service_exceptions = (OrganisationAddressServiceException, )
    update_form = UpdateOrganisationAddressForm
    create_form = CreateOrganisationAddressForm
    model = OrganisationAddress

    @classmethod
    def retrieve_organisation_address(cls, id: int) -> OrganisationAddress:
        """
        get an OrganisationAddress by id
        :param id: id of the OrganisationAddress
        :return: the OrganisationAddress object
        """
        try:
            org_address = cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            raise OrganisationEntityServiceException(
                "OrganisationAddress not found."
            )

        return org_address

    @classmethod
    def create_address(cls, user, name, street, city, postal_code, country):
        """
        create a new address object
        :param user: user calling the service
        :param name: name of the address e.g. "Hauptsitz"
        :param street: Street and houseno
        :param city: city name
        :param postal_code: postal code
        :param country: country 2digit iso code e.g. "DE"
        """

        if not user.has_perm(CanCreateOrganisationAddressPermission):
            raise PermissionError("You are not allowed to create an OrganisationAddress.")

        with reversion.create_revision():
            person = cls._create({"name": name,
                                  "street": street,
                                  "city": city,
                                  "postal_code": postal_code,
                                  "country": country})
            reversion.set_user(user)

    @classmethod
    def update_address(cls, user, address_id, name=NotPassed, street=NotPassed, city=NotPassed, postal_code=NotPassed,
                       country=NotPassed):
        """
        create a new address object
        :param user: user calling the service
        :param address_id: address_id of the address that should be updated
        :param name: name of the address e.g. "Hauptsitz"
        :param street: Street and houseno
        :param city: city name
        :param postal_code: postal code
        :param country: country 2digit iso code e.g. "DE"
        """

        organisation_address = cls.retrieve_organisation_address(address_id)

        if not user.has_perm(CanUpdateOrganisationAddressPermission, organisation_address):
            raise PermissionError("You are not allowed to update this OrganisationAddress object.")

        with reversion.create_revision():
            organisation_address = cls._update(
                organisation_address.pk,
                {
                    "name": name,
                    "street": street,
                    "city": city,
                    "postal_code": postal_code,
                    "country": country,
                },
            )
            reversion.set_user(user)
            reversion.set_comment(f"update via service by {user}")

        organisation_address.refresh_from_db()
        return organisation_address
