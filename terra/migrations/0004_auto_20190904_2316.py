# Generated by Django 2.2.3 on 2019-09-04 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("terra", "0003_employee_supervisor")]

    operations = [
        migrations.AddField(
            model_name="unit",
            name="type",
            field=models.CharField(
                choices=[
                    ("1", "Library"),
                    ("2", "Executive Division"),
                    ("3", "Managerial Unit"),
                    ("4", "Team"),
                ],
                default=3,
                max_length=1,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="unit",
            name="parent_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subteams",
                to="terra.Unit",
            ),
        ),
    ]