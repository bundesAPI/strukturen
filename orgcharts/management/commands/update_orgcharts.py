import hashlib
from io import BytesIO
from tempfile import NamedTemporaryFile

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.models.fields import files

from orgcharts.models import OrgChartURL, OrgChart


class Command(BaseCommand):
    help = 'Update the orgcharts'

    def handle(self, *args, **options):
        for url in OrgChartURL.objects.order_by("-created_at").all():
            m = hashlib.md5()
            blob = requests.get(url.url, stream=True)
            m.update(blob.content)
            try:
                OrgChart.objects.create(org_chart_url=url, document=files.File(ContentFile(blob.content), "orgchart.pdf"),
                                        document_hash=m.hexdigest())
            except IntegrityError:
                print("already stored")
