import json
import requests
import traceback
from bs4 import BeautifulSoup
from typing import Dict
from tqdm import tqdm
from urllib.parse import urljoin

import lib
from src.types.sources import SourceName
from src.types.resources import ResourceName
from src.crawler.base import CrawlerBase
from .magic import HUBS_TO_CRAWL
from .models import Article


class HabrPostsCrawler(CrawlerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HABR
    HOST = 'https://habr.com'
    ARTICLES_ENDPOINT_PATTERN = 'https://habr.com/ru/hub/programming/page{page_number}/'

    def __init__(self, *args, **kwargs):
        self.requester = lib.requesters.DefaultRequester(max_rps=10)
        super().__init__(*args, **kwargs)

    def crawl(self) -> None:
        for hub_url, ctx in tqdm(HUBS_TO_CRAWL, desc='Crawling habr posts — hubs', total=len(HUBS_TO_CRAWL), position=0):
            self.crawl_hub(hub_url, ctx)

    def crawl_hub(self, url, ctx: Dict):
        for page_number in tqdm(range(1, 51), desc='Crawling habr posts pages', total=50, leave=False, position=1):
            hub_page_url = urljoin(url, f'page{page_number}')
            self.crawl_hub_page(hub_page_url, ctx)

    def crawl_hub_page(self, url: str, ctx: Dict) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for article_tag in soup.select('article'):
            self.crawl_article(article_tag.select_one('a[class="tm-title__link"]')['href'], ctx)

    def crawl_article(self, article_path: str, ctx: Dict) -> None:
        try:
            self._crawl_article(article_path, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_path': article_path},
            }))

    def _crawl_article(self, article_path: str, ctx: Dict) -> None:
        url = HabrPostsCrawler.HOST + article_path
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tag = soup.select_one('article')
        article = Article.from_tag(article_tag, ctx={'url': url, 'response': response, 'soup': soup})
        self.write_output(article.json(ensure_ascii=False))
