import unittest
from src.ranker.post_ranker import PostRanker
from src.controller.posts.models import PostRecord


class TestPostRanker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_post_record = PostRecord(
            insert_timestamp=1684143421,
            resource_name='post',
            source_name='medium',
            canonized_url='https://medium.com/javascript-in-plain-english/the-best-of-angular-a-collection-of-my-favorite-articles-of-2022-8015cb63fbc2',
            original_url='https://medium.com/javascript-in-plain-english/the-best-of-angular-a-collection-of-my-favorite-articles-of-2022-8015cb63fbc2',
            title='The best of Angular: a collection of my favorite resources of 2022',
            topics=['development/frontend'],
            rank=20,
            starting_text='',
            publish_timestamp=1673989200,
            author_username='JavaScript in Plain English',
            views=None,
        )
        cls.real_features = {'clicks_count': 100}

    def test_smoke(self):
        _ = PostRanker()

    def test_rank(self):
        ranker = PostRanker()
        rank = ranker.rank(self.real_post_record, self.real_features)
        self.assertIsInstance(rank, int)

    def test_raw_rank(self):
        ranker = PostRanker()
        raw_rank = ranker.raw_rank(self.real_post_record, self.real_post_record.source_name)
        self.assertIsInstance(raw_rank, int)

    def test_features_bonus(self):
        ranker = PostRanker()
        features_bonus = ranker.features_bonus(self.real_features)
        self.assertIsInstance(features_bonus, int)

    def test__random_bonus(self):
        ranker = PostRanker()
        random_bonus = ranker._random_bonus(self.real_post_record)
        self.assertIsInstance(random_bonus, int)

    def test__age_penalty(self):
        ranker = PostRanker()
        age_penalty = ranker._age_penalty(self.real_post_record.publish_timestamp)
        self.assertIsInstance(age_penalty, int)

    def test__views_bonus(self):
        ranker = PostRanker()
        views_bonus = ranker._views_bonus(self.real_post_record.views or 0)
        self.assertIsInstance(views_bonus, int)
