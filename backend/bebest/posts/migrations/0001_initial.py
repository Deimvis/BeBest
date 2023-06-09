# Generated by Django 4.2.1 on 2023-05-15 09:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canonized_url', models.CharField(db_index=True, max_length=2048)),
                ('source_name', models.CharField(choices=[('habr', 'Habr')], max_length=128)),
                ('original_url', models.CharField(max_length=2048)),
                ('title', models.CharField(max_length=256)),
                ('topics', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), db_index=True, size=None)),
                ('rank', models.BigIntegerField()),
                ('starting_text', models.TextField()),
                ('publish_timestamp', models.BigIntegerField()),
                ('author_username', models.CharField(blank=True, max_length=128, null=True)),
                ('views', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
    ]
