import math
import random
import time
from typing import Dict
from src.types.sources import SourceName
from src.controller.posts.models import Post, PostRecord


class PostRanker:

    def rank(self, post: PostRecord, features: Dict) -> int:
        return self.raw_rank(post, post.source_name) + self.features_bonus(features) + self._random_bonus(post)

    def raw_rank(self, post: Post, source_name: str) -> int:
        """ rank[out]: [0, 1000] """
        initial_rank = 0
        match source_name:
            case SourceName.HABR:
                # boost for diversity
                initial_rank = 100
            case SourceName.MEDIUM:
                # initial_rank = 500
                # boost for diversity
                initial_rank = 900
            case SourceName.DCM:
                # initial_rank = 600
                # boost for diversity
                initial_rank = 1000
            case _:
                raise RuntimeError(f'Got unsupported source name: {post.source_name}')
        rank = initial_rank - self._age_penalty(post.publish_timestamp) + self._views_bonus(post.views or 0)
        return min(max(rank, 0), 1000)

    def features_bonus(self, features: Dict) -> int:
        bonus = 0
        if 'clicks_count' in features:
            bonus += features['clicks_count']
        return bonus

    def _random_bonus(self, post: Post) -> int:
        days_from_epoch = int(time.time()) // (12 * 3600)
        post_code = int.from_bytes(post.canonized_url.encode('utf-8'), byteorder='big')
        random.seed(days_from_epoch + post_code)
        return random.randint(0, 50)

    def _age_penalty(self, publish_timestamp: int) -> int:
        """
        10 days: penalty = 54
        20 days: penalty = 274
        30 days: penalty = 494
        60 days: penalty = 1994
        """
        days_left = (int(time.time()) - publish_timestamp) // (24 * 60 * 60)
        first_range = min(days_left, 10)
        first_penalty = first_range**2 - 2 * first_range * math.log(max(first_range, 1))
        second_range = max(days_left - 10, 0)
        second_penalty = 22 * second_range
        third_range = max(days_left - 30, 0)
        third_penalty = 50 * third_range
        return int(first_penalty + second_penalty + third_penalty)

    def _views_bonus(self, views: int) -> int:
        """
        0 views:      bonus = 0
        1k views:     bonus = 150
        100k views:   bonus = 250
        """
        return int(50 * math.log(views + 1, 10))
