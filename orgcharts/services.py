import reversion
from django.contrib.auth.models import AbstractUser
from serious_django_services import Service, NotPassed, CRUDMixin

from claims.services import RelationshipClaimService, ClaimService, ClaimTypeService
from organisation.forms import UpdateOrganisationEntityForm, CreateOrganisationEntityForm
from organisation.models import OrganisationEntity
from organisation.permissions import CanCreateOrganisationEntityPermission, CanUpdateOrganisationEntityPermission
from organisation.services import OrganisationEntityService
from orgcharts.forms import CreateOrgChartURLForm, UpdateOrgChartURLForm
from orgcharts.models import OrgChartURL, OrgChart, OrgChartStatusChoices
from orgcharts.permissions import CanCreateOrgChartURLPermission, CanImportOrgChartPermission
from person.services import PersonService
from settings import settings


class OrgChartURLServiceException(Exception):
    pass


class OrgChartImportServiceException(Exception):
    pass


class OrgChartServiceException(Exception):
    pass


class OrgChartURLService(Service, CRUDMixin):
    update_form = UpdateOrgChartURLForm
    create_form = CreateOrgChartURLForm

    service_exceptions = (OrgChartURLServiceException,)
    model = OrgChartURL

    @classmethod
    def retrieve_orgchart_url(cls, id: int) -> OrgChartURL:
        """
        get an OrgChartUrl by id
        :param id: id of the OrgChartUrl
        :return: the OrgChartUrl object
        """
        try:
            orgchart_url = cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            raise OrgChartURLServiceException(
                "OrgChartURL not found."
            )

        return orgchart_url

    @classmethod
    def create_orgchart_url(cls, user: AbstractUser, url: str, entity_id: int) -> OrgChartURL:
        """ create a new OrganisationEntity
            :param user: the user calling the service
            :param url: -  the url the orgchart can be found under
            :param entity_id: -  sid of the organisation entity
            :returns: the newly created OrgChartUrl instance
        """

        if not user.has_perm(CanCreateOrgChartURLPermission):
            raise PermissionError("You are not allowed to create an OrgChartUrl.")

        with reversion.create_revision():
            org_chart_url = cls._create({"url": url, "organisation_entity": entity_id})
            reversion.set_user(user)

        return org_chart_url


class OrgChartService(Service):
    service_exceptions = (OrgChartServiceException,)
    model = OrgChart

    @classmethod
    def retrieve_orgchart(cls, id: int) -> OrgChart:
        """
        get an OrgChart by id
        :param id: id of the OrgChartUrl
        :return: the OrgChart object
        """
        try:
            orgchart = cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            raise OrgChartServiceException(
                "OrgChart not found."
            )

        return orgchart


class OrgChartImportService(Service):
    service_exceptions = (OrgChartImportServiceException,)

    SOURCE_URI = "ORGCHARTIMPORT_FROM_PDF:"

    @classmethod
    def import_organisation_entity(cls, user, orgchart_entity, parent, orgchart_id):

        if "parsed" not in orgchart_entity or "id" not in orgchart_entity:
            raise OrgChartImportServiceException(f"You tried to import an entity without any parsed data")
        import_src_id = cls.SOURCE_URI + str(orgchart_id) + ":" + orgchart_entity["id"]

        for entity in orgchart_entity["parsed"]["organisations"]:
            print(entity)
            if "short_name" not in entity:
                entity["short_name"] = ""
            curr_organisation = OrganisationEntityService.create_organisation_entity(user,
                                                                                     short_name=entity[
                                                                                         "short_name"],
                                                                                     name=entity["name"],
                                                                                     parent_id=parent.id)
            for person in entity["people"]:
                curr_person = PersonService.create_person(user,
                                                          person["name"],
                                                          person["position"])
                claim = RelationshipClaimService.create_relationship_claim(user, curr_person.pk,
                                                                           ClaimTypeService.resolve_claim_type_by_codename(
                                                                               settings.CLAIMS["LEADS"]).pk,
                                                                           curr_organisation.pk
                                                                           )
            if "children" in orgchart_entity and orgchart_entity["children"]:
                for item in orgchart_entity["children"]:
                    cls.import_organisation_entity(user, item, curr_organisation, orgchart_id)

    @classmethod
    def import_parsed_orgchart(cls, user: AbstractUser, orgchart_id: int, orgchart):
        """ initial parsing import of an orgchart pdf
        :param orgchart_id: the id the orgchart_id that should be imported
        :param orgchart: the orgchart object as Dict

        """
        if not user.has_perm(CanImportOrgChartPermission):
            raise PermissionError("You are not allowed to do initial orgchart imports.")

        orgchart_document = OrgChartService.retrieve_orgchart(orgchart_id)
        if orgchart_document.status not in [OrgChartStatusChoices.NEW, OrgChartStatusChoices.PARSED]:
            raise OrgChartImportServiceException(f"Orgchart needs to be in status '{OrgChartStatusChoices.NEW}' to be "
                                                 f"imported")

        if orgchart_document != orgchart_document.org_chart_url.orgchart_documents.order_by("-id").first():
            raise OrgChartImportServiceException(f"This is not the latest Orgchart available. Please try to import "
                                                 f"the latest version")

        if orgchart_document.org_chart_url.orgchart_documents.filter(
                status__in=[OrgChartStatusChoices.IMPORTED]).first() is not None:
            raise OrgChartImportServiceException(
                f"For the Organisation '{orgchart_document.org_chart_url.organisation_entity.name}' the initial "
                f"import is already done.")

        if len(orgchart) == 0:
            raise OrgChartImportServiceException(f"Nothing to import! Json body seems to be empty")

        # update the raw source field for the document
        orgchart_document.raw_source = orgchart
        orgchart_document.save()

        organisation = orgchart_document.org_chart_url.organisation_entity

        for entity in orgchart:
            cls.import_organisation_entity(user, entity, organisation, orgchart_id)

        orgchart_document.status = OrgChartStatusChoices.IMPORTED
        orgchart_document.save()

        return orgchart_document
