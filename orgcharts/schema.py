import graphene
from django.http import request
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from graphql_relay.connection.connectiontypes import Connection
from graphene_file_upload.scalars import Upload
from serious_django_graphene import (
    FailableMutation,
    get_user_from_info,
    MutationExecutionException,
)
from serious_django_services import NotPassed

from orgcharts.models import OrgChartURL, OrgChart, OrgChartError, OrgChartStatusChoices
from orgcharts.permissions import (
    CanCreateOrgChartURLPermission,
    CanImportOrgChartPermission,
)
from orgcharts.services import (
    OrgChartURLService,
    OrgChartService,
    OrgChartImportService,
    OrgChartErrorService,
)

OrgChartStatus = graphene.Enum.from_enum(OrgChartStatusChoices)


class OrgChartURLNode(DjangoObjectType):
    class Meta:
        model = OrgChartURL
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class OrgChartNode(DjangoObjectType):
    class Meta:
        model = OrgChart
        filter_fields = ["id"]
        interfaces = (relay.Node,)

    def resolve_document(self, info):
        return self.document.url


class OrgChartErrorNode(DjangoObjectType):
    class Meta:
        model = OrgChartError
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CreateOrgChartURL(FailableMutation):
    org_chart_url = graphene.Field(OrgChartURLNode)

    class Arguments:
        url = graphene.String(required=True)
        entity_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateOrgChartURLPermission])
    def mutate(self, info, url, entity_id):
        user = get_user_from_info(info)
        try:
            result = OrgChartURLService.create_orgchart_url(
                user, url=url, entity_id=int(from_global_id(entity_id)[1])
            )
        except OrgChartURLService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrgChartURL(success=True, organisation_entity=result)


class CreateOrgChartError(FailableMutation):
    org_chart_error = graphene.Field(OrgChartErrorNode)

    class Arguments:
        message = graphene.String(required=True)
        org_chart_url_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateOrgChartURLPermission])
    def mutate(self, info, message, org_chart_url_id):
        user = get_user_from_info(info)
        try:
            result = OrgChartErrorService.create_orgchart_error(
                user,
                org_chart_url_id=int(from_global_id(org_chart_url_id)[1]),
                message=message,
            )
        except OrgChartErrorService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrgChartError(success=True, org_chart_error=result)


class CreateOrgChart(FailableMutation):
    org_chart = graphene.Field(OrgChartNode)

    class Arguments:
        document_hash = graphene.String(required=True)
        org_chart_url_id = graphene.ID(required=True)
        document = Upload(required=True)

    @permissions_checker([IsAuthenticated, CanCreateOrgChartURLPermission])
    def mutate(self, info, document_hash, org_chart_url_id, document):
        user = get_user_from_info(info)
        try:
            result = OrgChartService.create_orgchart(
                user,
                org_chart_url_id=int(from_global_id(org_chart_url_id)[1]),
                document_hash=document_hash,
                document=document,
            )
        except OrgChartService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrgChart(success=True, org_chart=result)


class ImportOrgChart(FailableMutation):
    org_chart = graphene.Field(OrgChartNode)

    class Arguments:
        orgchart_id = graphene.ID(required=True)
        raw_json = graphene.JSONString(required=True)

    @permissions_checker([IsAuthenticated, CanImportOrgChartPermission])
    def mutate(self, info, orgchart_id, raw_json):
        user = get_user_from_info(info)
        try:
            result = OrgChartImportService.import_parsed_orgchart(
                user, orgchart_id=int(from_global_id(orgchart_id)[1]), orgchart=raw_json
            )
        except OrgChartImportService.exceptions as e:
            raise MutationExecutionException(str(e))
        return ImportOrgChart(success=True, org_chart=result)


class UpdateOrgChart(FailableMutation):
    org_chart = graphene.Field(OrgChartNode)

    class Arguments:
        org_chart_id = graphene.ID(required=True)
        raw_source = graphene.JSONString(required=True)
        status = OrgChartStatus(required=True)

    @permissions_checker([IsAuthenticated, CanImportOrgChartPermission])
    def mutate(self, info, org_chart_id, raw_source, status):
        user = get_user_from_info(info)
        try:
            result = OrgChartService.update_orgchart(
                user,
                org_chart_id=int(from_global_id(org_chart_id)[1]),
                raw_source=raw_source,
                status=status,
            )
        except OrgChartService.exceptions as e:
            raise MutationExecutionException(str(e))
        return UpdateOrgChart(success=True, org_chart=result)


class Query(graphene.ObjectType):
    all_org_chart_urls = DjangoFilterConnectionField(OrgChartURLNode)
    org_chart_url = relay.Node.Field(OrgChartURLNode)
    all_org_charts = DjangoFilterConnectionField(OrgChartNode)
    org_chart = relay.Node.Field(OrgChartNode)


class Mutation(graphene.ObjectType):
    create_org_chart_url = CreateOrgChartURL.Field()
    import_org_chart = ImportOrgChart.Field()
    create_org_chart_error = CreateOrgChartError.Field()
    create_org_chart = CreateOrgChart.Field()
    update_org_chart = UpdateOrgChart.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
