import unittest
from src.scrapers.posts.hackernoon.utils import update_url_params


class TestUpdateUrlParams(unittest.TestCase):

    def test_smoke(self):
        _ = update_url_params('https://github.com/Deimvis', {})

    def test_simple(self):
        self.assertEqual(update_url_params('https://github.com/Deimvis', {}), 'https://github.com/Deimvis')
        self.assertEqual(update_url_params('https://github.com/Deimvis', {'key': 'value'}), 'https://github.com/Deimvis?key=value')
        self.assertEqual(update_url_params('https://github.com/Deimvis?key=badvalue', {'key': 'value'}), 'https://github.com/Deimvis?key=value')
        self.assertEqual(update_url_params('https://github.com/Deimvis', {'key': 123}), 'https://github.com/Deimvis?key=123')
