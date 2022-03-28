import boto3
from django.conf import settings
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


def get_search_client() -> OpenSearch:
    # TODO: remove me and move to the opensearch-django-dsl
    credentials = boto3.session.Session(
        region_name=settings.AWS_EB_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    ).get_credentials()
    auth = AWSV4SignerAuth(credentials, settings.AWS_EB_DEFAULT_REGION)
    client = OpenSearch(
        hosts=[{"host": settings.OPEN_SEARCH_CLUSTER_ENDPOINT, "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    return client
