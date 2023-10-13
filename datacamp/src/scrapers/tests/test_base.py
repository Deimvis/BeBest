import unittest
import lib
from typing import Type
from src.scrapers.base import ScraperBase
from src.scrapers.plan_base import ScrapePlanBase
from src.types import ResourceName, SourceName


class TestScraperBase(unittest.TestCase):

    def setUp(self):
        self.output_consumer = lib.consumers.DummyConsumer()
        self.logs_consumer = lib.consumers.DummyConsumer()

    def _init(self, cls: Type[ScraperBase]) -> ScraperBase:
        return cls(output_consumer=self.output_consumer, logs_consumer=self.logs_consumer)

    def test_smoke(self):
        MyScraper = type('MyScraper', (ScraperBase,), {
            'scrape': lambda self, *args, **kwargs: None,
            'RESOURCE_NAME': ResourceName.POST,
            'SOURCE_NAME': SourceName.HABR,
            'plan_type': ScrapePlanBase,
        })
        _ = self._init(MyScraper)

    def test_invalid_implementation(self):
        with self.assertRaises(TypeError):
            MyScraper = type('MyScraper', (ScraperBase,), {})
            _ = self._init(MyScraper)

        with self.assertRaises(TypeError):
            MyScraper = type('MyScraper', (ScraperBase,), {
                'scrape': lambda self, *args, **kwargs: None,
            })
            _ = self._init(MyScraper)

        with self.assertRaises(TypeError):
            MyScraper = type('MyScraper', (ScraperBase,), {
                'RESOURCE_NAME': ResourceName.POST,
                'SOURCE_NAME': SourceName.HABR,
            })
            _ = self._init(MyScraper)
