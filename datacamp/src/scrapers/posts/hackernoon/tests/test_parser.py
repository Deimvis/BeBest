import os
import requests
import unittest
from bs4 import BeautifulSoup
from src.scrapers.posts.hackernoon.parser import HackernoonArticleParser


class TestHackernoonArticleParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_soup = cls._get_soup('https://hackernoon.com/lite/what-the-heck-is-sdf')

    def test_smoke(self):
        _ = HackernoonArticleParser(soup=self.real_soup)

    def test_parse_author_username(self):
        parser = HackernoonArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_author_username(), 'ProgRockRec')

    def test_parse_publish_date(self):
        parser = HackernoonArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_publish_date(), '2023/10/24')

    def test_parse_tags(self):
        parser = HackernoonArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_tags(), ['programming', 'dbt', 'data-engineering', 'sql', 'what-is-sdf', 'semantic-data-fabric', 'data', 'compiler-and-build-system'])

    def test_parse_title(self):
        parser = HackernoonArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_title(), 'What the Heck Is SDF?')

    @classmethod
    def _get_soup(cls, url):
        proxies = {
            'http': os.getenv('REQUESTS_HTTP_PROXY'),
            'https': os.getenv('REQUESTS_HTTPS_PROXY'),
        }
        return BeautifulSoup(requests.get(url, proxies=proxies).text, 'html.parser')
