# Generated by Django 4.2.1 on 2023-05-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_alter_vacancystats_salary_from_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VacancyArea',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=256)),
                ('city_name', models.CharField(max_length=256)),
            ],
        ),
    ]