# Generated by Django 3.1.2 on 2020-10-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0004_auto_20201021_1245'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prognosedemission',
            unique_together={('Minutes5DK', 'PriceArea')},
        ),
        migrations.CreateModel(
            name='Emission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Minutes5DK', models.DateTimeField()),
                ('CO2Emission', models.IntegerField()),
                ('PriceArea', models.CharField(default='', max_length=5)),
            ],
            options={
                'unique_together': {('Minutes5DK', 'PriceArea')},
            },
        ),
    ]
