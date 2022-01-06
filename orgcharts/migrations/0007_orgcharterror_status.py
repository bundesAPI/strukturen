# Generated by Django 3.2.10 on 2022-01-06 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orgcharts", "0006_orgcharterror"),
    ]

    operations = [
        migrations.AddField(
            model_name="orgcharterror",
            name="status",
            field=models.CharField(
                choices=[("NEW", "new"), ("RESOLVED", "resolved")],
                default="NEW",
                max_length=20,
            ),
        ),
    ]
