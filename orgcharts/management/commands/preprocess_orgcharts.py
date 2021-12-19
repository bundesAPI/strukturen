import hashlib
from io import BytesIO
from tempfile import NamedTemporaryFile

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.models.fields import files
from graphql_relay import to_global_id

from orgcharts.models import OrgChartURL, OrgChart, OrgChartStatusChoices
from orgcharts.schema import OrgChartNode


class Command(BaseCommand):
    help = "Parse new orgcharts"

    def handle(self, *args, **options):
        for org_chart in OrgChart.objects.filter(
            status__in=[OrgChartStatusChoices.NEW]
        ):
            try:
                # yeah its not nice but it does the job
                orgchart_global_id = to_global_id(OrgChartNode.__name__, org_chart.id)
                orgchart_data = requests.get(
                    f"{settings.ML_BACKEND_BASE_URL}/analyze-orgchart/",
                    params={"orgchart_id": orgchart_global_id, "page": 0},
                )
                print(orgchart_data)
                org_chart.raw_source = orgchart_data.json()
                org_chart.status = OrgChartStatusChoices.PARSED
                org_chart.save()
            except Exception as e:
                print(e)
