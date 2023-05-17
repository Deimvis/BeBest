from .base import CrawlerBase  # noqa
from .manager import CrawlersManager  # noqa
from .posts import HabrPostsCrawler, MediumPostCrawler, DCMPostCrawler  # noqa
from .vacancies import HHAPIVacanciesCrawler  # noqa


ALL_CRAWLERS = [HabrPostsCrawler, MediumPostCrawler, DCMPostCrawler, HHAPIVacanciesCrawler]
crawlers_manager = CrawlersManager(ALL_CRAWLERS)
