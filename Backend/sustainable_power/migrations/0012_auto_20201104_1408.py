# Generated by Django 3.1.2 on 2020-11-04 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0011_auto_20201030_2037'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='default_emission',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='default_price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='value',
            name='device',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sustainable_power.device'),
        ),
        migrations.AlterUniqueTogether(
            name='emission',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='prognosedemission',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='prognosedprice',
            unique_together=set(),
        ),
    ]
