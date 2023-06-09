# Generated by Django 4.2.1 on 2023-05-21 19:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatacampArea',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=256)),
                ('city_name', models.CharField(max_length=256)),
                ('hh_id', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'datacamp__area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DatacampVacancyStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=128)),
                ('speciality', models.CharField(max_length=256)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), size=None)),
                ('salary', models.JSONField()),
            ],
            options={
                'db_table': 'datacamp_vacancy_stats',
                'managed': False,
            },
        ),
    ]
