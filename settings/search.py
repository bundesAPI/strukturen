import boto3
from django.conf import settings
from opensearchpy import AWSV4SignerAuth, OpenSearch


def get_search_client() -> OpenSearch:
    credentials = boto3.session.Session(
        region_name=settings.AWS_EB_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    ).get_credentials()
    auth = AWSV4SignerAuth(credentials, settings.AWS_SECRETS_MANAGER_REGION_NAME)
    client = OpenSearch(
        hosts=[{"host": settings.OPEN_SEARCH_CLUSTER_ENDPOINT, "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=settings.RequestsHttpConnection,
    )
    return client
