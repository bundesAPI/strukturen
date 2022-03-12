# Generated by Django 3.2.11 on 2022-02-28 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0004_alter_person_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="persons",
                to="person.positionabbreviation",
            ),
        ),
    ]