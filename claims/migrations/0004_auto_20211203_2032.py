# Generated by Django 3.2.9 on 2021-12-03 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("claims", "0003_auto_20211203_2007"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="claim",
            options={"base_manager_name": "objects"},
        ),
        migrations.AlterModelOptions(
            name="relationshipclaim",
            options={"base_manager_name": "objects"},
        ),
        migrations.AlterModelOptions(
            name="valueclaim",
            options={"base_manager_name": "objects"},
        ),
        migrations.AddField(
            model_name="claim",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_claims.claim_set+",
                to="contenttypes.contenttype",
            ),
        ),
    ]
