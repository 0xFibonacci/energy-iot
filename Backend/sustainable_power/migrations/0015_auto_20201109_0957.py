# Generated by Django 3.1.2 on 2020-11-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0014_auto_20201104_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
