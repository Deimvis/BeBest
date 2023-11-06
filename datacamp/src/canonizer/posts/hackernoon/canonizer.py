import json
import traceback
from datetime import datetime
from src.canonizer import helpers

from src.types.sources import SourceName
from src.types import ResourceName
from src.canonizer.base import CanonizerBase
from src.controller.posts.models import RawPost, Post
from src.scrapers.posts.hackernoon.models import Article
from src.ranker import PostRanker
from .topics import match_to_topics


class HackernoonPostsCanonizer(CanonizerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HACKERNOON

    def __init__(self, *args, **kwargs):
        self.post_ranker = PostRanker()
        super().__init__(*args, **kwargs)

    def canonize(self, data: str) -> None:
        article = Article(**json.loads(data))
        try:
            post = self._canonize(article)
            self.write_output(post.model_dump())
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': article.url},
            }))

    def _canonize(self, article: Article) -> Post:
        canonized_url = helpers.canonize_url(article.url)
        publish_timestamp = self._canonize_date(article.publish_date)
        topics = match_to_topics(article)
        raw_post = RawPost(
            canonized_url=canonized_url,
            original_url=article.url,
            title=article.title,
            topics=topics,
            starting_text=article.starting_text,
            publish_timestamp=publish_timestamp,
            author_username=article.author_username,
        )
        rank = self.post_ranker.raw_rank(raw_post, self.SOURCE_NAME)
        post = Post(**(raw_post.model_dump() | dict(rank=rank)))
        return post

    def _canonize_date(self, date: str) -> int:
        return int(datetime.strptime(date, '%Y/%m/%d').timestamp())
