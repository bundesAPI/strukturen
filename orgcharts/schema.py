import graphene
from django.http import request
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from graphql_relay.connection.connectiontypes import Connection
from serious_django_graphene import FailableMutation, get_user_from_info, MutationExecutionException
from serious_django_services import NotPassed

from orgcharts.models import OrgChartURL, OrgChart
from orgcharts.permissions import CanCreateOrgChartURLPermission, CanImportOrgChartPermission
from orgcharts.services import OrgChartURLService, OrgChartService, OrgChartImportService


class OrgChartURLNode(DjangoObjectType):
    class Meta:
        model = OrgChartURL
        filter_fields = ['id']
        interfaces = (relay.Node,)

class OrgChartNode(DjangoObjectType):
    class Meta:
        model = OrgChart
        filter_fields = ['id']
        interfaces = (relay.Node,)

    def resolve_document(self, info):
        return self.document.url

class CreateOrgChartURL(FailableMutation):
    org_chart_url = graphene.Field(OrgChartURLNode)

    class Arguments:
        url = graphene.String(required=True)
        entity_id = graphene.ID(required=True)

    @permissions_checker([IsAuthenticated, CanCreateOrgChartURLPermission])
    def mutate(self, info, url, entity_id):
        user = get_user_from_info(info)
        try:
            result = OrgChartURLService.create_orgchart_url(user, url=url, entity_id=int(from_global_id(entity_id)[1]))
        except OrgChartURLService.exceptions as e:
            raise MutationExecutionException(str(e))
        return CreateOrgChartURL(success=True, organisation_entity=result)


class ImportOrgChart(FailableMutation):
    org_chart = graphene.Field(OrgChartNode)

    class Arguments:
        orgchart_id = graphene.ID(required=True)
        raw_json = graphene.JSONString(required=True)

    @permissions_checker([IsAuthenticated, CanImportOrgChartPermission])
    def mutate(self, info, orgchart_id, raw_json):
        user = get_user_from_info(info)
        try:
            result = OrgChartImportService.import_parsed_orgchart(user, orgchart_id=int(from_global_id(orgchart_id)[1]),
                                                                  orgchart=raw_json)
        except OrgChartImportService.exceptions as e:
            raise MutationExecutionException(str(e))
        return ImportOrgChart(success=True, org_chart=result)


class Query(graphene.ObjectType):
    all_org_chart_urls = DjangoFilterConnectionField(OrgChartURLNode)
    org_chart_url = relay.Node.Field(OrgChartURLNode)
    all_org_charts = DjangoFilterConnectionField(OrgChartNode)
    org_chart = relay.Node.Field(OrgChartNode)


class Mutation(graphene.ObjectType):
    create_org_chart_url = CreateOrgChartURL.Field()
    import_org_chart = ImportOrgChart.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
