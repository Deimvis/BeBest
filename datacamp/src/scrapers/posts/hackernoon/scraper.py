import os
import logging
import json
import requests
import traceback
from typing import Dict, Type
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait

import lib
from lib.utils.logging import logging_on_call
from src.types import ResourceName, SourceName
from src.scrapers.base import ScraperBase
from src.scrapers.plan_base import ScrapePlanBase
# from .chrome_driver import chrome_driver
from .models import Article
from .parser import HackernoonArticleParser
from .plan import HackernoonPostsScrapePlan
# from .utils import update_url_params


log_ = logging.getLogger(__name__)


class HackernoonPostsScraper(ScraperBase):
    RESOURCE_NAME = ResourceName.POST
    SOURCE_NAME = SourceName.HACKERNOON
    BASE_URL = 'https://hackernoon.com'
    LITE_ARTICLE_URL_PATTERN = BASE_URL + '/lite{path}'

    def __init__(self, *args, **kwargs):
        proxies = {
            'http': os.getenv('REQUESTS_HTTP_PROXY'),
            'https': os.getenv('REQUESTS_HTTPS_PROXY'),
        }
        requester_ = lib.requesters.DefaultRequester(max_rps=1, proxies=proxies)
        cache_ = lib.storages.cache.LRUCache(max_size=32)
        self.requester = lib.requesters.CachedRequester(requester=requester_, cache=cache_)
        # self.chrome_driver = None  # NOTE: see note below
        super().__init__(*args, **kwargs)

    # NOTE: usual scraping approach doesn't work
    #       since article cards doesn't load even with chrome driver and proxy
    #       they do load though under vpn
    #       but reason of these events is unclear
    # def scrape(self, plan: HackernoonPostsScrapePlan) -> None:
    #     with chrome_driver(use_proxy=True) as driver:
    #         self.chrome_driver = driver
    #         for tag in tqdm(plan.tags, desc='Scraping tags', total=len(plan.tags), position=0, leave=True):
    #             self.scrape_tag(tag.url, tag.page_count, ctx={})
    #         self.chrome_driver = None

    # @logging_on_call('Scrape tag: {url}', logging.DEBUG, logger=log_)
    # def scrape_tag(self, url: str, page_count: int, ctx: Dict):
    #     for page_number in tqdm(range(1, 1+page_count), desc='Scraping tag pages', total=page_count, leave=False, position=1):
    #         tag_page_url = update_url_params(url, {'page': page_number})
    #         self.scrape_tag_page(tag_page_url, ctx)

    # def scrape_tag_page(self, url: str, ctx: Dict):
    #     try:
    #         self._scrape_tag_page(url, ctx)
    #     except Exception as error:
    #         self.write_error(json.dumps({
    #             'error': str(error),
    #             'traceback': traceback.format_exc(),
    #             'context': {'tag_url': url},
    #         }))

    # def _scrape_tag_page(self, url: str, ctx: Dict):
    #     self.chrome_driver.get(url)
    #     wait = WebDriverWait(self.chrome_driver, timeout=15)
    #     wait.until(lambda d: len(self.chrome_driver.find_elements(By.TAG_NAME, 'article')) == 12)
    #     soup = BeautifulSoup(self.chrome_driver.page_source, 'html.parser')
    #     for article_tag in soup.select('article'):
    #         a_tag = article_tag.select_one('h2').select_one('a')
    #         if a_tag.has_attr('rel') and a_tag['rel'] == ['sponsored']: continue
    #         self.scrape_article(urljoin(url, a_tag['href']), ctx)

    def scrape(self, plan: HackernoonPostsScrapePlan) -> None:
        for tag in tqdm(plan.tags, desc='Scraping tags', total=len(plan.tags), position=0, leave=True):
            self.scrape_tag(tag.name, tag.page_count, ctx={})

    @logging_on_call('Scrape tag: {tag_name}', logging.DEBUG, logger=log_)
    def scrape_tag(self, tag_name: str, page_count: int, ctx: Dict):
        for page_ind in tqdm(range(page_count), desc='Scraping tag pages', total=page_count, leave=False, position=1):
            self.scrape_tag_page(tag_name, page_ind, ctx)

    def scrape_tag_page(self, tag_name: str, page_ind: int, ctx: Dict):
        try:
            self._scrape_tag_page(tag_name, page_ind, ctx)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'tag_name': tag_name, 'page_ind': page_ind},
            }))

    def _scrape_tag_page(self, tag_name: str, page_ind: int, ctx: Dict):
        response = self._request_tag_page(tag_name, page_ind)
        data = response.json()
        for article in data['results'][0]['hits']:
            article_url = f'{self.BASE_URL}/{article["slug"]}'
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
        lite_article_url = self.LITE_ARTICLE_URL_PATTERN.format(path=urlparse(url).path)
        soup = BeautifulSoup(self.requester.get(lite_article_url).text, 'html.parser')
        article = self._parse_article(soup, ctx)
        self.write_output(article.model_dump_json())

    def _parse_article(self, soup: BeautifulSoup, ctx: Dict) -> Article:
        parser = HackernoonArticleParser(soup)
        parser.TRY_PARSE_EVERYTHING()
        parsing_results = parser.GET_PARSING_RESULTS()
        article = Article(**(ctx | parsing_results))
        return article

    @classmethod
    def plan_type(cls) -> Type[ScrapePlanBase]:
        return HackernoonPostsScrapePlan

    def _request_tag_page(self, tag_name: str, page_ind: int) -> requests.Response:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en-RU;q=0.9,en-GB;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://hackernoon.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        data = json.dumps({
            "requests": [
                {
                    "indexName": "stories",
                    "params": f"clickAnalytics=true&facetFilters=%5B%22tags%3A{tag_name}%22%5D&facets=%5B%22tags%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=11&maxValuesPerFacet=10&page={page_ind}&query=&tagFilters=",
                }
            ]
        })
        return self.requester.post(
            'https://mo7dwh9y8c-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.11.1)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.38.1)&x-algolia-api-key=e0088941fa8f9754226b97fa87a7c340&x-algolia-application-id=MO7DWH9Y8C',
            headers=headers,
            data=data,
        )
