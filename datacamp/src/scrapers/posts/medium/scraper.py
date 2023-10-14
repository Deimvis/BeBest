import os
import logging
import json
import traceback
from typing import Dict, Type
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit

import lib
from lib.utils.logging import logging_on_call
from src.types import ResourceName, SourceName
from src.scrapers.base import ScraperBase
from src.scrapers.plan_base import ScrapePlanBase
from .models import Article
from .parser import ArticleParser
from .plan import MediumPostsScrapePlan


log_ = logging.getLogger(__name__)


class MediumPostsScraper(ScraperBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.MEDIUM

    def __init__(self, *args, **kwargs):
        proxies = {
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY'),
        }
        requester_ = lib.requesters.DefaultRequester(max_rps=1, proxies=proxies)
        cache_ = lib.storages.cache.LRUCache(max_size=32)
        self.requester = lib.requesters.CachedRequester(requester=requester_, cache=cache_)
        super().__init__(*args, **kwargs)

    def scrape(self, plan: MediumPostsScrapePlan) -> None:
        for blog in plan.blogs:
            self.scrape_blog(blog.url, ctx=blog.model_dump())

    @logging_on_call('Scrape blog: {url}', logging.DEBUG, logger=log_)
    def scrape_blog(self, url: str, ctx: Dict):
        try:
            self._scrape_blog(url, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'blog_url': url},
            }))

    def _scrape_blog(self, url: str, ctx: Dict):
        response = self.requester.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_candidates = soup.select('a:has(h1), a:has(h2), a:has(h3), a:has(h4), a:has(h5), a:has(h6)')
        for a_tag in tqdm(article_candidates, desc='Scraping article candidates', total=len(article_candidates), position=1, leave=False):
            article_url = a_tag['href']
            normalized_article_url = urlunsplit((
                urlparse(url).scheme,
                urlparse(url).netloc,
                urlparse(article_url).path,
                None,
                None,
            ))
            article_soup = BeautifulSoup(self.requester.get(normalized_article_url).text, 'html.parser')
            if len(article_soup.select('h1[data-testid="storyTitle"]')) == 1:
                self.scrape_article(normalized_article_url, ctx)

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
        parser = ArticleParser(soup)
        parser.TRY_PARSE_EVERYTHING()
        parsing_results = parser.GET_PARSING_RESULTS()
        article = Article(**(ctx | parsing_results))
        return article

    @classmethod
    def plan_type(cls) -> Type[ScrapePlanBase]:
        return MediumPostsScrapePlan
