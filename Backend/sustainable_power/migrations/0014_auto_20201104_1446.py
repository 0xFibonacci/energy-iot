# Generated by Django 3.1.2 on 2020-11-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0013_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='preferred_emission',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='preferred_price',
            field=models.FloatField(null=True),
        ),
    ]
