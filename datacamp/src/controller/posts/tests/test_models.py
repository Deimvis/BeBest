import unittest
from src.controller.posts.models import PostRecord


class TestPostRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_post_row = {
            'insert_timestamp': 1684143421,
            'resource_name': 'post',
            'source_name': 'medium',
            'canonized_url': 'https://medium.com/javascript-in-plain-english/the-best-of-angular-a-collection-of-my-favorite-articles-of-2022-8015cb63fbc2',
            'original_url': 'https://medium.com/javascript-in-plain-english/the-best-of-angular-a-collection-of-my-favorite-articles-of-2022-8015cb63fbc2',
            'title': 'The best of Angular: a collection of my favorite resources of 2022',
            'topics': ['development/frontend'],
            'rank': 20, 'starting_text': '',
            'publish_timestamp': 1673989200,
            'author_username': 'JavaScript in Plain English',
            'views': None,
        }
        cls.real_post_record_kwargs = dict(
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

    def test_smoke(self):
        _ = PostRecord(**self.real_post_record_kwargs)

    def test_unique_key(self):
        post_record = PostRecord(**self.real_post_record_kwargs)
        expected = {
            'resource_name': self.real_post_record_kwargs['resource_name'],
            'source_name': self.real_post_record_kwargs['source_name'],
            'canonized_url': self.real_post_record_kwargs['canonized_url'],
        }
        result = post_record.unique_key()
        self.assertEqual(expected, result)

    def test_to_database_row(self):
        post_record = PostRecord(**self.real_post_record_kwargs)
        self.assertEqual(post_record.to_database_row(), self.real_post_row)

    def test_from_database_row(self):
        post_record = PostRecord.from_database_row(self.real_post_row)
        self.assertEqual(post_record, PostRecord(**self.real_post_record_kwargs))
