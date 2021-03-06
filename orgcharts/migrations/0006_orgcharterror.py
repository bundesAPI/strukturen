# Generated by Django 3.2.10 on 2022-01-06 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orgcharts", "0005_alter_orgchart_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrgChartError",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "org_chart_url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="errors",
                        to="orgcharts.orgcharturl",
                    ),
                ),
            ],
        ),
    ]
