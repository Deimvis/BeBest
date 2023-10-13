import unittest
from src.scrapers.base import ScraperBase
from src.scrapers.manager import ScrapersManager
from src.scrapers.plan_base import ScrapePlanBase
from src.types import ResourceName, SourceName


class TestScrapersManager(unittest.TestCase):

    def test_smoke(self):
        _ = ScrapersManager([])

    def test_find_Scraper(self):
        MyScraper = type('MyScraper', (ScraperBase,), {
            'scrape': lambda self: None,
            'RESOURCE_NAME': ResourceName.POST,
            'SOURCE_NAME': SourceName.HABR,
            'plan_type': ScrapePlanBase,
        })
        manager = ScrapersManager([MyScraper])
        self.assertEqual(manager.find_Scraper(ResourceName.POST, SourceName.HABR), MyScraper)

    def test_similar_Scrapers(self):
        MyScraper1 = type('MyScraper', (ScraperBase,), {
            'scrape': lambda self: False,
            'RESOURCE_NAME': ResourceName.POST,
            'SOURCE_NAME': SourceName.HABR,
            'plan_type': ScrapePlanBase,
        })
        MyScraper2 = type('MyScraper', (ScraperBase,), {
            'scrape': lambda self: True,
            'RESOURCE_NAME': ResourceName.POST,
            'SOURCE_NAME': SourceName.HABR,
            'plan_type': ScrapePlanBase,
        })
        manager = ScrapersManager([MyScraper1, MyScraper2])
        self.assertEqual(manager.find_Scraper(ResourceName.POST, SourceName.HABR), MyScraper2)
