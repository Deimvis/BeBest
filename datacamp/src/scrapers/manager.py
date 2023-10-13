from collections import defaultdict
from typing import Iterable, Type
from src.types.sources import SourceName
from src.types import ResourceName
from .base import ScraperBase


class ScrapersManager:
    def __init__(self, Scrapers: Iterable[Type[ScraperBase]]):
        self._Scrapers = Scrapers
        self._resource_name2source_name2Scraper = defaultdict(dict)
        for Scraper in Scrapers:
            self._resource_name2source_name2Scraper[Scraper.RESOURCE_NAME][Scraper.SOURCE_NAME] = Scraper

    def find_Scraper(self, resource_name: str, source_name: str) -> Type[ScraperBase]:
        def validate_input():
            nonlocal self, resource_name, source_name
            if resource_name not in ResourceName.values():
                raise RuntimeError(f'Got unsupported resource name: `{resource_name}`')
            if source_name not in SourceName.values():
                raise RuntimeError(f'Got unsupported source_name name: `{source_name}`')
            if resource_name not in self.resource_name2source_name2Scraper:
                raise RuntimeError(f'Has no Scrapers for resource name: `{resource_name}`')
            if source_name not in self.resource_name2source_name2Scraper[resource_name]:
                raise RuntimeError(f'Has no Scrapers for source_name name: `{source_name}` (resource_name = `{resource_name}`)')

        validate_input()
        return self.resource_name2source_name2Scraper[resource_name][source_name]

    @property
    def Scrapers(self):
        return self._Scrapers

    @property
    def resource_name2source_name2Scraper(self):
        return self._resource_name2source_name2Scraper
