import json
import requests
import traceback
from tqdm import tqdm
from bs4 import BeautifulSoup

from lib.sources import SourceName
from lib.resources import ResourceName
from src.crawler.base import CrawlerBase
from .models import Article


class HabrPostsCrawler(CrawlerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HABR
    HOST = 'https://habr.com'
    ARTICLES_ENDPOINT_PATTERN = 'https://habr.com/ru/hub/programming/page{page_number}/'

    def crawl(self) -> None:
        for page_number in tqdm(range(1, 51), desc='Crawling habr posts pages', total=50, leave=False):
            self.crawl_articles_page(page_number)

    def crawl_articles_page(self, page_number: int) -> None:
        url = HabrPostsCrawler.ARTICLES_ENDPOINT_PATTERN.format(**dict(page_number=page_number))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for article_tag in soup.select('article'):
            self.crawl_article(article_tag.select_one('a[class="tm-title__link"]')['href'])

    def crawl_article(self, article_path: str) -> None:
        try:
            self._crawl_article(article_path)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_path': article_path},
            }))

    def _crawl_article(self, article_path: str) -> None:
        url = HabrPostsCrawler.HOST + article_path
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tag = soup.select_one('article')
        article = Article.from_tag(article_tag, ctx={'url': url, 'response': response, 'soup': soup})

        self.write_output(article.json(ensure_ascii=False))

        # TODO: write Requester
        import time
        time.sleep(0.5)
