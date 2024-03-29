import logging
import json
import requests
import traceback
from bs4 import BeautifulSoup
from typing import Dict
from tqdm import tqdm
from urllib.parse import urljoin

import lib
from lib.utils.logging import logging_on_call
from src.types.sources import SourceName
from src.types import ResourceName
from src.scrapers.base import ScraperBase
from .models import Article
from .parser import HabrPostsParser
from .plan import HabrPostsScrapePlan


log_ = logging.getLogger(__name__)


class HabrPostsScraper(ScraperBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HABR
    HOST = 'https://habr.com'
    ARTICLES_ENDPOINT_PATTERN = 'https://habr.com/ru/hub/programming/page{page_number}/'

    def __init__(self, *args, **kwargs):
        self.requester = lib.requesters.DefaultRequester(max_rps=10)
        super().__init__(*args, **kwargs)

    def scrape(self, plan: HabrPostsScrapePlan) -> None:
        for hub in tqdm(plan.hubs, desc='Scraping habr hubs', total=len(plan.hubs), position=0):
            self.scrape_hub(hub.url, hub.page_count, ctx={'hubs': [hub.hub_name] if hub.hub_name else []})

    @logging_on_call('Scrape hub: {url}', logging.DEBUG, logger=log_)
    def scrape_hub(self, url: str, page_count: int, ctx: Dict):
        for page_number in tqdm(range(1, 1+page_count), desc='Scraping habr posts pages', total=page_count, leave=False, position=1):
            hub_page_url = urljoin(url, f'page{page_number}')
            self.scrape_hub_page(hub_page_url, ctx)

    @logging_on_call('Scrape hub page: {url}', logging.DEBUG, logger=log_)
    def scrape_hub_page(self, url: str, ctx: Dict) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for article_tag in soup.select('article'):
            self.scrape_article(HabrPostsScraper.HOST + article_tag.select_one('a[class="tm-title__link"]')['href'], ctx)

    @logging_on_call('Scrape article: {url}', logging.DEBUG, logger=log_)
    def scrape_article(self, url: str, ctx: Dict) -> None:
        try:
            self._scrape_article(url, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'url': url},
            }))

    def _scrape_article(self, url: str, ctx: Dict) -> None:
        ctx['url'] = url
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = self._parse_article(soup, ctx)
        self.write_output(article.model_dump_json())

    def _parse_article(self, soup: BeautifulSoup, ctx: Dict) -> Article:
        parser = HabrPostsParser(soup)
        parser.TRY_PARSE_EVERYTHING()
        parsing_results = parser.GET_PARSING_RESULTS()
        article = Article(**(ctx | parsing_results))
        return article

    @classmethod
    def plan_type(cls):
        return HabrPostsScrapePlan
