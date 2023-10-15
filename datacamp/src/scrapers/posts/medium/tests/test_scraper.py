import unittest
import lib
from typing import Dict, Sequence
from unittest import mock
from src.scrapers.posts.medium.scraper import MediumPostsScraper
from src.scrapers.posts.medium.plan import MediumPostsScrapePlan


class TestMediumPostsScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patchers = [
            mock.patch('src.scrapers.posts.medium.scraper.tqdm', lambda iterable, *args, **kwargs: iterable),
        ]
        for p in cls.patchers:
            p.start()

    @classmethod
    def tearDownClass(cls):
        for p in cls.patchers:
            p.stop()

    def test_smoke(self):
        _ = MediumPostsScraper(output_consumer=lib.consumers.DummyConsumer(), logs_consumer=lib.consumers.DummyConsumer())

    def test_scrape(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            scraper = MediumPostsScraper(output_consumer=output_consumer, logs_consumer=logs_consumer)
            plan = MediumPostsScrapePlan(blogs=[MediumPostsScrapePlan.Blog(url='https://netflixtechblog.medium.com/', publisher='Netflix Technology Blog')])
            scraper.scrape(plan)
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertGreater(len(output), 0)
            self.assertEqual(self._count_errors(logs), 0)

    def test_scrape_article(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            scraper = MediumPostsScraper(output_consumer=output_consumer, logs_consumer=logs_consumer)
            url = 'https://netflixtechblog.com/zero-configuration-service-mesh-with-on-demand-cluster-discovery-ac6483b52a51?source=collection_home---4------0-----------------------'
            scraper.scrape_article(url, ctx={'url': url})
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertEqual(len(output), 1)
            self.assertEqual(self._count_errors(logs), 0)

    def _count_errors(self, logs: Sequence[Dict]):
        cnt = 0
        for log in logs:
            cnt += log['level'] == 'ERROR'
        return cnt
