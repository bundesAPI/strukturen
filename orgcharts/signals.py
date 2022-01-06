import json

import boto3
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from graphql_relay import to_global_id

from orgcharts.models import OrgChart, OrgChartStatusChoices, OrgChartURL
from orgcharts.schema import OrgChartNode, OrgChartURLNode


@receiver(post_save, sender=OrgChartURL)
def start_orgchart_analysis(sender, instance, created, **kwargs):

    if created and settings.ORGCHART_CRAWLER_SNS_TOPIC is not None:
        client = boto3.client("sns", settings.AWS_EB_DEFAULT_REGION)
        message = {
            "action": "crawl-orgchart",
            "parameters": {
                "org_chart_url_id": to_global_id(OrgChartURLNode.__name__, instance.pk)
            },
        }
        print(message)
        response = client.publish(
            TopicArn=settings.ORGCHART_CRAWLER_SNS_TOPIC, Message=json.dumps(message)
        )
        print(response)


@receiver(post_save, sender=OrgChart)
def start_orgchart_analysis(sender, instance, created, **kwargs):
    if (
        instance.status == OrgChartStatusChoices.NEW
        and settings.ORGCHART_ANALYSIS_SNS_TOPIC is not None
    ):
        client = boto3.client("sns", settings.AWS_EB_DEFAULT_REGION)
        message = {
            "action": "analyze-orgchart",
            "parameters": {
                "orgchart_id": to_global_id(OrgChartNode.__name__, instance.pk),
                "page": 0,  # TODO: fixme
            },
        }
        print("message")
        response = client.publish(
            TopicArn=settings.ORGCHART_ANALYSIS_SNS_TOPIC, Message=json.dumps(message)
        )
