# Generated by Django 2.2.5 on 2019-10-10 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0005_auto_20191007_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='terra.Unit'),
        ),
    ]
