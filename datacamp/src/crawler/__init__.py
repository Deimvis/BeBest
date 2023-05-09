from .base import CrawlerBase  # noqa
from .manager import CrawlersManager  # noqa
from .posts import HabrPostsCrawler  # noqa


ALL_CRAWLERS = [HabrPostsCrawler]
crawlers_manager = CrawlersManager(ALL_CRAWLERS)
