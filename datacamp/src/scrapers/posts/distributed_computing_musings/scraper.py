import logging
import json
import traceback
from typing import Dict
from tqdm import tqdm
from bs4 import BeautifulSoup

import lib
from lib.utils.logging import logging_on_call
from src.types.sources import SourceName
from src.types import ResourceName
from src.scrapers.base import ScraperBase
from .models import Article
from .parser import Parser
from .plan import DCMPostsScrapePlan


log_ = logging.getLogger(__name__)


class DCMPostsScraper(ScraperBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.DCM

    ARTICLES_ENDPOINT_PATTERN = 'https://distributed-computing-musings.com/page/{page_number}/'

    def __init__(self, *args, **kwargs):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'whoami': 'https://bebest.pro/'}
        self.requester = lib.requesters.DefaultRequester(headers=headers)
        super().__init__(*args, **kwargs)

    def scrape(self, plan: DCMPostsScrapePlan) -> None:
        for page_number in tqdm(range(1, 1+plan.page_count), desc='Scraping distributed-computing-musings posts — pages', total=plan.page_count, position=0):
            self.scrape_articles_page(page_number, {})

    def scrape_articles_page(self, page_number: int, ctx: Dict):
        import logging
        logging.error('get url %s', self.ARTICLES_ENDPOINT_PATTERN.format(**dict(page_number=page_number)))
        response = self.requester.get(self.ARTICLES_ENDPOINT_PATTERN.format(**dict(page_number=page_number)))
        soup = BeautifulSoup(response.text, 'html.parser')
        for article in tqdm(soup.select('article[id]'), desc='Scraping distributed-computing-musings posts', leave=False, position=1):
            article_url = article.find_all('a', rel=None)[0]['href']
            self.scrape_article(article_url, ctx)

    @logging_on_call('Scrape article: {url}', logging.DEBUG, logger=log_)
    def scrape_article(self, url: str, ctx: Dict) -> None:
        try:
            self._scrape_article(url, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': url},
            }))

    def _scrape_article(self, url: str, ctx: Dict) -> None:
        ctx['url'] = url
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = self._parse_article(soup, ctx)
        self.write_output(article.model_dump_json())

    def _parse_article(self, soup: BeautifulSoup, ctx: Dict) -> Article:
        parser = Parser(soup)
        parser.TRY_PARSE_EVERYTHING()
        parsing_results = parser.GET_PARSING_RESULTS()
        article = Article(**(ctx | parsing_results))
        return article

    @classmethod
    def plan_type(cls):
        return DCMPostsScrapePlan
