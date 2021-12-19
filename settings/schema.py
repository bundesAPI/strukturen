import graphene
from claims import schema as claims_schema
from person import schema as person_schema
from organisation import schema as organisation_schema
from orgcharts import schema as orgcharts_schema
from oauth import schema as oauth_schema


class Query(claims_schema.schema.Query, orgcharts_schema.Query, oauth_schema.Query, organisation_schema.Query,
            graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(person_schema.Mutation, organisation_schema.Mutation, orgcharts_schema.Mutation, claims_schema.Mutation,
               oauth_schema.Mutation):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
