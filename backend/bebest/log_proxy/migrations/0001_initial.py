# Generated by Django 4.2.1 on 2023-05-15 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.BigIntegerField()),
                ('username', models.CharField(max_length=150, null=True)),
                ('action', models.CharField(choices=[('go_to', 'Go To')], max_length=32)),
                ('action_value', models.CharField(max_length=1024, null=True)),
            ],
        ),
    ]
