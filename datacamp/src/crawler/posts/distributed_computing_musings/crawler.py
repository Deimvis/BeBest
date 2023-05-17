import json
import traceback
from typing import Dict
from tqdm import tqdm
from bs4 import BeautifulSoup

import lib
from lib.sources import SourceName
from lib.resources import ResourceName
from src.crawler.base import CrawlerBase
from .models import Article
from .parser import Parser


class DCMPostCrawler(CrawlerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.DCM

    ARTICLES_ENDPOINT_PATTERN = 'https://distributed-computing-musings.com/page/{page_number}/'

    def __init__(self, *args, **kwargs):
        self.requester = lib.requesters.DefaultRequester()
        super().__init__(*args, **kwargs)

    def crawl(self) -> None:
        for page_number in tqdm(range(1, 6), desc='Crawling distributed-computing-musings posts — pages', total=5, position=0):
            self.crawl_articles_page(page_number, {})

    def crawl_articles_page(self, page_number: int, ctx: Dict):
        response = self.requester.get(self.ARTICLES_ENDPOINT_PATTERN.format(**dict(page_number=page_number)))
        soup = BeautifulSoup(response.text, 'html.parser')
        for article in tqdm(soup.select('article[id]'), desc='Crawling distributed-computing-musings posts', leave=False, position=1):
            article_url = article.find_all('a', rel=None)[0]['href']
            self.crawl_article(article_url, ctx)

    def crawl_article(self, url: str, ctx: Dict) -> None:
        try:
            self._crawl_article(url, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': url},
            }))

    def _crawl_article(self, url: str, ctx: Dict) -> None:
        ctx['url'] = url
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = self._parse_article(soup, ctx)
        self.write_output(article.json(ensure_ascii=False))

    def _parse_article(self, soup: BeautifulSoup, ctx: Dict) -> Article:
        parser = Parser(soup)
        parser.try_parse_EVERYTHING()
        parsing_results = parser.get_parsing_results()
        article = Article(**(ctx | parsing_results))
        return article
