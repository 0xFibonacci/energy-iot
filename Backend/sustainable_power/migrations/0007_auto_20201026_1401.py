# Generated by Django 3.1.2 on 2020-10-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0006_auto_20201023_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]
