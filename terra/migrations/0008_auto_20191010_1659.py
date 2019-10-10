# Generated by Django 2.2.5 on 2019-10-10 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("terra", "0007_auto_20191010_1653")]

    operations = [
        migrations.AlterField(
            model_name="fund",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="terra.Unit",
            ),
        )
    ]
