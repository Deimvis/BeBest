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
        assert resource_name in ResourceName.all()
        assert source_name in SourceName.all()
        return self.resource_name2source_name2Crawler[resource_name][source_name]

    @property
    def Crawlers(self):
        return self._Crawlers

    @property
    def resource_name2source_name2Crawler(self):
        return self._resource_name2source_name2Crawler
