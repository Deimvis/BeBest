import django.contrib.postgres.fields as postgres_fields
from django.db import models
from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    class SourceName(models.TextChoices):
        HABR = 'habr'

    canonized_url = models.CharField(max_length=2048, db_index=True)
    source_name = models.CharField(max_length=128, choices=SourceName.choices)
    original_url = models.CharField(max_length=2048)
    title = models.CharField(max_length=256)
    topics = postgres_fields.ArrayField(models.CharField(max_length=256))
    rank = models.BigIntegerField()
    starting_text = models.TextField()
    publish_timestamp = models.BigIntegerField()
    author_username = models.CharField(max_length=128, blank=True, null=True)
    views = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'Post({self.id}, canonized_url={self.canonized_url})'

    @staticmethod
    def example() -> 'Post':
        from django.utils import timezone
        return Post(
            canonized_url='https://test.com/path',
            source_name='habr',
            original_url='https://test.com/path?flag=true',
            title='MyTitle',
            topics=['development'],
            rank=1,
            starting_text='my text',
            publish_timestamp=int(timezone.now().timestamp()),
            author_username='admin',
            views=0,
        )
