# Generated by Django 2.2.5 on 2019-09-26 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacation',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]