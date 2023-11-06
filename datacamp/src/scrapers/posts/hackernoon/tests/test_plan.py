import unittest
from pydantic import ValidationError
from src.scrapers.posts.hackernoon.plan import HackernoonPostsScrapePlan


class TestHackernoonPostsScraper(unittest.TestCase):

    def test_smoke(self):
        _ = HackernoonPostsScrapePlan(tags=[])

    def test_simple_tags(self):
        _ = HackernoonPostsScrapePlan(tags=[
            HackernoonPostsScrapePlan.Tag(name='programming'),
            HackernoonPostsScrapePlan.Tag(name='data-science'),
        ])
