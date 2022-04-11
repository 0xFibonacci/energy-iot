# Generated by Django 3.1.2 on 2020-10-17 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainable_power', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ready', models.BooleanField()),
                ('completed_before', models.DateTimeField()),
                ('energy_consumption', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PrognosedPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('price', models.FloatField()),
                ('area', models.CharField(default='', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_max_value', models.FloatField()),
                ('pref_min_value', models.FloatField()),
                ('value', models.FloatField()),
            ],
        ),
    ]
