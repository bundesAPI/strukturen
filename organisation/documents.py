from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry

from organisation.models import OrganisationEntity


@registry.register_document
class OrganisationEntityDocument(Document):
    class Index:
        name = "organisations"  # Name of the Opensearch index
        settings = {  # See Opensearch Indices API reference for available settings
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        # Configure how the index should be refreshed after an update.
        # See Opensearch documentation for supported options.
        # This per-Document setting overrides settings.OPENSEARCH_DSL_AUTO_REFRESH.
        auto_refresh = False

    class Django:
        model = OrganisationEntity
        queryset_pagination = 128
        fields = [
            "name",
            "short_name",
        ]

    id = fields.LongField()
    locations = fields.NestedField(
        properties={
            "id": fields.LongField(),
            "name": fields.KeywordField(),
            "street": fields.KeywordField(),
            "city": fields.KeywordField(),
            "postal_code": fields.KeywordField(),
            "country": fields.KeywordField(),
            "phone_prefix": fields.KeywordField(),
        }
    )
