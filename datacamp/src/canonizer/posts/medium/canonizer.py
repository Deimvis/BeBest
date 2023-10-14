import json
import traceback
import re
import regex_spm
from datetime import datetime
from src.canonizer import helpers

from src.types.sources import SourceName
from src.types import ResourceName
from src.canonizer.base import CanonizerBase
from src.controller.posts.models import RawPost, Post
from src.scrapers.posts.medium.models import Article
from src.ranker import PostRanker
from .topics import match_to_topics


class MediumPostsCanonizer(CanonizerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.MEDIUM

    def __init__(self, *args, **kwargs):
        self.post_ranker = PostRanker()
        super().__init__(*args, **kwargs)

    def canonize(self, data: str) -> None:
        article = Article(**json.loads(data))
        try:
            self._canonize(article)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': article.url},
            }))

    def _canonize(self, article: Article) -> None:
        canonized_url = helpers.canonize_url(article.url)
        publish_timestamp = self._canonize_date(article.publish_date)
        # TODO: fix parsed publish_date for articles from https://medium.com/google-cloud (`2 days ago` instead of date)
        topics = match_to_topics(article)
        raw_post = RawPost(
            canonized_url=canonized_url,
            original_url=article.url,
            title=article.title,
            topics=topics,
            starting_text='',
            publish_timestamp=publish_timestamp,
            author_username=article.publisher,
        )
        rank = self.post_ranker.raw_rank(raw_post, self.SOURCE_NAME)
        post = Post(**(raw_post.model_dump() | dict(rank=rank)))
        self.write_output(post.model_dump())

    def _canonize_date(self, date_str: str) -> int:
        date_str = date_str.strip()
        match regex_spm.fullmatch_in(date_str):
            case r'^[A-Z][a-z]{2} \d{1,2}, \d{4}':
                match_result = re.match(r'^(?P<month>[A-Z][a-z]{2}) (?P<day>\d{1,2}), (?P<year>\d{4})', date_str)
                dt = datetime.strptime(match_result.group('month'), '%b')
                dt = dt.replace(day=int(match_result.group('day')))
                dt = dt.replace(year=int(match_result.group('year')))
            case r'^[A-Z][a-z]{2} \d{1,2}':
                match_result = re.match(r'^(?P<month>[A-Z][a-z]{2}) (?P<day>\d{1,2})', date_str)
                dt = datetime.strptime(match_result.group('month'), '%b')
                dt = dt.replace(day=int(match_result.group('day')))
                dt = dt.replace(year=datetime.now().year)
            case _:
                raise RuntimeError(f'Got unsupported date string format: {date_str}')
        return int(dt.timestamp())

    def _canonize_views(self, views: str | None) -> int | None:
        if views is None:
            return None
        if views.endswith('K'):
            return int(float(views[:-1]) * 1000)
        else:
            return int(views)
