import unittest
import lib
from unittest import mock
from typing import Dict, Sequence
from src.scrapers.posts.habr import HabrPostsScraper
from src.scrapers.posts.habr.plan import HabrPostsScrapePlan


class TestHabrPostsScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patchers = [
            mock.patch('tqdm.tqdm', lambda iterable, *args, **kwargs: iterable),
        ]
        for p in cls.patchers:
            p.start()

    @classmethod
    def tearDownClass(cls):
        for p in cls.patchers:
            p.stop()

    def setUp(self):
        self.output_consumer = lib.consumers.DummyConsumer()
        self.logs_consumer = lib.consumers.DummyConsumer()

    def test_smoke(self):
        _ = HabrPostsScraper(output_consumer=self.output_consumer, logs_consumer=self.logs_consumer)

    def test_scrape(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            scraper = HabrPostsScraper(output_consumer=output_consumer, logs_consumer=logs_consumer)
            plan = HabrPostsScrapePlan(hubs=[HabrPostsScrapePlan.Hub(url='https://habr.com/ru/hub/programming/', page_count=1)])
            scraper.scrape(plan)
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertGreater(len(output), 0)
            self.assertEqual(self._count_errors(logs), 0)

    def test_scrape_article(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            scraper = HabrPostsScraper(output_consumer=output_consumer, logs_consumer=logs_consumer)
            url = 'https://habr.com/ru/articles/722688/'
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
