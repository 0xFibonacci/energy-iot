# Generated by Django 3.1.2 on 2020-11-11 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0017_auto_20201111_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='allowed_on_time',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='device',
            name='bluetooth_address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
