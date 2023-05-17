import json
import traceback
import re
import regex_spm
from datetime import datetime
from src.canonizer import helpers

from lib.sources import SourceName
from lib.resources import ResourceName
from lib.specialities import Speciality
from src.canonizer.base import CanonizerBase
from src.controller.posts.model import RawPost, Post
from src.crawler.posts.distributed_computing_musings.models import Article
from src.ranker import PostRanker


class DCMPostsCanonizer(CanonizerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.DCM

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
        raw_post = RawPost(
            canonized_url=canonized_url,
            original_url=article.url,
            title=article.title,
            topics=[Speciality.DEVELOPMENT.BACKEND],
            starting_text=article.starting_text,
            publish_timestamp=publish_timestamp,
            author_username='Distributed Computing Missings',
        )
        rank = self.post_ranker.raw_rank(raw_post, self.SOURCE_NAME)
        post = Post(**(raw_post.dict() | dict(rank=rank)))
        self.write_output(post.dict())

    def _canonize_date(self, date_str: str) -> int:
        date_str = date_str.strip()
        match regex_spm.fullmatch_in(date_str):
            case r'^[A-Z][a-z]+ \d{1,2}, \d{4}':
                match_result = re.match(r'^(?P<month>[A-Z][a-z]+) (?P<day>\d{1,2}), (?P<year>\d{4})', date_str)
                dt = datetime.strptime(match_result.group('month'), '%B')
                dt = dt.replace(day=int(match_result.group('day')))
                dt = dt.replace(year=int(match_result.group('year')))
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
