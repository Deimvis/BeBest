import os
import requests
import unittest
from bs4 import BeautifulSoup
from pathlib import Path
from src.scrapers.posts.medium.parser import MediumArticleParser


class TestMediumArticleParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_soup = cls._get_soup('https://netflixtechblog.com/zero-configuration-service-mesh-with-on-demand-cluster-discovery-ac6483b52a51')

    def test_smoke(self):
        _ = MediumArticleParser()

    def test_parse_title(self):
        parser = MediumArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_title(), 'Zero Configuration Service Mesh with On-Demand Cluster Discovery')

    def test_parse_author_username(self):
        parser = MediumArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_author_username(), 'Netflix Technology Blog')

    def test_parse_publisher(self):
        parser = MediumArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_publisher(), 'Netflix TechBlog')

    def test_parse_publish_date(self):
        parser = MediumArticleParser(soup=self.real_soup)
        self.assertIn(parser.parse_publish_date(), ['Aug 29', 'Aug 30', 'Aug 31'])
        parser = MediumArticleParser(soup=BeautifulSoup((Path(os.getenv('FILES_DIR_PATH')) / 'test_data' / 'medium_article__1dayago.html').read_text(), 'html.parser'))
        self.assertEqual(parser.parse_publish_date(), '1 day ago')

    def test_parse_tags(self):
        parser = MediumArticleParser(soup=self.real_soup)
        self.assertEqual(parser.parse_tags(), ['Envoy', 'Service Mesh', 'Microservices', 'Ipc', 'Cloud'])
        parser = MediumArticleParser(soup=self._get_soup('https://medium.com/google-cloud/understanding-bigquery-connector-for-saps-compression-feature-969a438c668d'))
        self.assertEqual(parser.parse_tags(), ['Google Cloud Platform', 'Bigquery', 'Data'])
        parser = MediumArticleParser(soup=self._get_soup('https://medium.angularaddicts.com/switching-newsletter-platforms-angular-addicts-dea4e917caaf'))
        self.assertEqual(parser.parse_tags(), [])

    @classmethod
    def _get_soup(cls, url):
        proxies = {
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY'),
        }
        return BeautifulSoup(requests.get(url, proxies=proxies).text, 'html.parser')
