from collections import defaultdict
from typing import Iterable, Type
from lib.sources import SourceName
from lib.resources import ResourceName
from .base import CrawlerBase


class CrawlersManager:
    def __init__(self, Crawlers: Iterable[Type[CrawlerBase]]):
        self._Crawlers = Crawlers
        self._resource_name2source_name2Crawler = defaultdict(dict)
        for Crawler in Crawlers:
            self._resource_name2source_name2Crawler[Crawler.RESOURCE_NAME][Crawler.SOURCE_NAME] = Crawler

    def find_Crawler(self, resource_name: str, source_name: str) -> Type[CrawlerBase]:
        def validate_input():
            nonlocal self, resource_name, source_name
            if resource_name not in ResourceName.values():
                raise RuntimeError(f'Got unsupported resource name: `{resource_name}`')
            if source_name not in SourceName.values():
                raise RuntimeError(f'Got unsupported source_name name: `{source_name}`')
            if resource_name not in self.resource_name2source_name2Crawler:
                raise RuntimeError(f'Has no Crawlers for resource name: `{resource_name}`')
            if source_name not in self.resource_name2source_name2Crawler[resource_name]:
                raise RuntimeError(f'Has no Crawlers for source_name name: `{source_name}` (resource_name = `{resource_name}`)')

        validate_input()
        return self.resource_name2source_name2Crawler[resource_name][source_name]

    @property
    def Crawlers(self):
        return self._Crawlers

    @property
    def resource_name2source_name2Crawler(self):
        return self._resource_name2source_name2Crawler
