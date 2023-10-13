from .base import ScraperBase  # noqa
from .manager import ScrapersManager  # noqa
from .posts import HabrPostsScraper, MediumPostsScraper, DCMPostsScraper  # noqa
from .vacancies import HHAPIVacanciesScraper  # noqa


ALL_CRAWLERS = [HabrPostsScraper, MediumPostsScraper, DCMPostsScraper, HHAPIVacanciesScraper]
scrapers_manager = ScrapersManager(ALL_CRAWLERS)
