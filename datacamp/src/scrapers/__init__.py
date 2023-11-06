from .base import ScraperBase  # noqa
from .manager import ScrapersManager  # noqa
from .posts import HabrPostsScraper, HackernoonPostsScraper, MediumPostsScraper, DCMPostsScraper  # noqa
from .vacancies import HHAPIVacanciesScraper  # noqa


ALL_CRAWLERS = [HabrPostsScraper, HackernoonPostsScraper, MediumPostsScraper, DCMPostsScraper, HHAPIVacanciesScraper]
scrapers_manager = ScrapersManager(ALL_CRAWLERS)
