import json
import traceback
from datetime import datetime
from src.canonizer import helpers

from lib.sources import SourceName
from lib.resources import ResourceName
from src.canonizer.base import CanonizerBase
from src.controller.posts.model import RawPost, Post
from src.crawler.posts.habr.models import Article
from src.ranker import PostRanker
from .topics import match_to_topics


class HabrPostsCanonizer(CanonizerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HABR

    def __init__(self, *args, **kwargs):
        self.post_ranker = PostRanker()
        super().__init__(*args, **kwargs)

    def canonize(self, data: str) -> None:
        article = Article(**json.loads(data))
        try:
            post = self._canonize(article)
            self.write_output(post.dict())
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': article.url},
            }))

    def _canonize(self, article: Article) -> Post:
        canonized_url = helpers.canonize_url(article.url)
        publish_timestamp = self._canonize_datetime(article.publish_datetime)
        views = self._canonize_views(article.views)
        topics = match_to_topics(article)
        raw_post = RawPost(
            canonized_url=canonized_url,
            original_url=article.url,
            title=article.title,
            topics=topics,
            starting_text=article.starting_text,
            publish_timestamp=publish_timestamp,
            author_username=article.author_username,
            views=views,
        )
        rank = self.post_ranker.raw_rank(raw_post, self.SOURCE_NAME)
        post = Post(**(raw_post.dict() | dict(rank=rank)))
        return post

    def _canonize_datetime(self, dt_str: str) -> int:
        return int(datetime.fromisoformat(dt_str).timestamp())

    def _canonize_views(self, views: str | None) -> int | None:
        if views is None:
            return None
        if views.endswith('K'):
            return int(float(views[:-1]) * 1000)
        else:
            return int(views)
