# Generated by Django 3.2.10 on 2022-01-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0005_organisationaddress_phone_prefix"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisationaddress",
            name="phone_prefix",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
