import unittest
from src.scrapers import scrapers_manager
from src.types import ResourceName, SourceName


class TestScrapersManager(unittest.TestCase):

    def test_smoke(self):
        self.assertGreater(len(scrapers_manager.Scrapers), 0)

    def test_scrapers_are_reachable(self):
        _ = scrapers_manager.find_Scraper(ResourceName.POST, SourceName.HABR)
        _ = scrapers_manager.find_Scraper(ResourceName.POST, SourceName.MEDIUM)
        _ = scrapers_manager.find_Scraper(ResourceName.POST, SourceName.DCM)
        _ = scrapers_manager.find_Scraper(ResourceName.VACANCY, SourceName.HH_API)
