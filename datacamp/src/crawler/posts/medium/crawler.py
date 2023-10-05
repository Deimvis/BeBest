import json
import re
import requests
import traceback
from typing import Dict
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit

import lib
from lib.sources import SourceName
from lib.resources import ResourceName
from src.crawler.base import CrawlerBase
from .magic import BLOGS_TO_CRAWL
from .models import Article
from .parser import Parser


class MediumPostCrawler(CrawlerBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.MEDIUM

    def __init__(self, *args, **kwargs):
        self.requester = lib.requesters.DefaultRequester(max_rps=1)
        super().__init__(*args, **kwargs)

    def crawl(self) -> None:
        for url, ctx in tqdm(BLOGS_TO_CRAWL, desc='Crawling medium posts — blogs', total=len(BLOGS_TO_CRAWL), position=0):
            self.crawl_blog(url, ctx)

    def crawl_blog(self, url: str, ctx: Dict):
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('a[aria-label="Post Preview Title"][href]')
        for a_tag in tqdm(articles, desc='Crawling medium posts', total=len(articles), position=1, leave=False):
            article_url = a_tag['href']
            normalized_article_url = urlunsplit((
                urlparse(url).scheme,
                urlparse(url).netloc,
                urlparse(article_url).path,
                None,
                None,
            ))
            self.crawl_article(normalized_article_url, ctx)

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
