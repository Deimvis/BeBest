import json
import traceback
from typing import List
from tqdm import tqdm
from bs4 import BeautifulSoup

import lib
from src.types.sources import SourceName
from src.types import ResourceName
from src.scrapers.base import ScraperBase
from .magic import CRAWL_AREAS, CRAWL_REQUESTS
from . import api_models, models


class HHAPIVacanciesScraper(ScraperBase):
    RESOURCE_NAME = ResourceName.VACANCY
    SOURCE_NAME = SourceName.HH_API
    API_ENDPOINT = 'https://api.hh.ru'
    VACANCIES_ENDPOINT = API_ENDPOINT + '/vacancies'
    HEADERS = {'HH-User-Agent': 'BeBest/0.1 (star_maps@mail.ru)'}
    PER_PAGE = 20
    TOTAL_PAGES = 10

    def __init__(self, *args, **kwargs):
        self.requester = lib.requesters.DefaultRequester(max_rps=1)
        super().__init__(*args, **kwargs)

    def scrape(self) -> None:
        for area_id in tqdm(CRAWL_AREAS, desc='Scraping hh_api vacancies — areas', total=len(CRAWL_AREAS), leave=True, position=0):
            self.scrape_area(area_id)

    def scrape_area(self, area_id: int) -> None:
        for request in tqdm(CRAWL_REQUESTS, desc='Scraping hh_api vacancies - requests', total=len(CRAWL_REQUESTS), leave=True, position=1):
            search_text = request['search_text']
            speciality = request['speciality']
            tags = request['tags']
            self.scrape_vacancies(area_id, search_text, speciality, tags)

    def scrape_vacancies(self, area_id: int, search_text: int, speciality: str, tags: List) -> None:
        for page_ind in tqdm(range(self.TOTAL_PAGES), desc='Scraping hh_api vacancies - pages', total=self.TOTAL_PAGES, leave=False, position=2):
            self.scrape_vacancies_page(area_id, search_text, speciality, tags, page_ind)

    def scrape_vacancies_page(self, area_id: int, search_text: int, speciality: str, tags: List, page_ind: int) -> None:
        try:
            self._scrape_vacancies_page(area_id, search_text, speciality, tags, page_ind)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'area_id': area_id, 'search_text': search_text, 'page_ind': page_ind},
            }, ensure_ascii=False))

    def _scrape_vacancies_page(self, area_id: int, search_text: int, speciality: str, tags: List, page_ind: int) -> None:
        url = self.VACANCIES_ENDPOINT
        response = self.requester.get(url, params={'area': area_id, 'text': search_text, 'page_ind': page_ind, 'per_page': self.PER_PAGE}, headers=self.HEADERS)
        vacancies_response = api_models.VacanciesResponse.parse_raw(response.text)
        for vacancy_resp in vacancies_response.items:
            vacancy = models.Vacancy.from_api_model(vacancy_resp, speciality, tags)
            self.write_output(vacancy.json(by_alias=True))
