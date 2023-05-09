import django.contrib.postgres.fields as postgres_fields
from django.db import models
from posts.models import Post


class ExportLog(models.Model):
    source_table_name = models.CharField(max_length=256)
    destination_table_name = models.CharField(max_length=256)
    timestamp =  models.BigIntegerField()


class DatacampPost(models.Model):
    insert_timestamp = models.BigIntegerField(blank=True, null=True)
    resource_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    canonized_url = models.CharField(max_length=2048, primary_key=True)
    original_url = models.CharField(max_length=2048)
    title = models.CharField(max_length=256)
    topics = postgres_fields.ArrayField(models.CharField(max_length=256))
    rank = models.BigIntegerField()
    starting_text = models.TextField()
    publish_timestamp = models.BigIntegerField()
    author_username = models.CharField(max_length=128, blank=True, null=True)
    views = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datacamp_post'
