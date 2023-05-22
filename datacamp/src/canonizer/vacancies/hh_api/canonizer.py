import json
import traceback
from datetime import datetime
from src.canonizer import helpers

from lib.sources import SourceName
from lib.resources import ResourceName
from src.canonizer.base import CanonizerBase
from src.controller.vacancies.model import Vacancy
from src.crawler.vacancies.hh_api.api_models import Area as APIArea
from src.crawler.vacancies.hh_api.models import Vacancy as CrawledVacancy
from src.ranker import PostRanker


class HHAPIPostsCanonizer(CanonizerBase):
    RESOURCE_NAME = ResourceName.VACANCY
    SOURCE_NAME = SourceName.HH_API

    def __init__(self, *args, **kwargs):
        self.post_ranker = PostRanker()
        super().__init__(*args, **kwargs)

    def canonize(self, data: str) -> None:
        crawled_vacancy = CrawledVacancy(**json.loads(data))
        try:
            self._canonize(crawled_vacancy)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'article_url': crawled_vacancy.url},
            }))

    def _canonize(self, crawled_vacancy: CrawledVacancy) -> None:
        original_url = crawled_vacancy.alternate_url
        canonized_url = helpers.canonize_url(original_url)
        api_url = crawled_vacancy.url
        title = crawled_vacancy.name
        area_id = self._get_area_id(crawled_vacancy.area)
        salary = crawled_vacancy.salary
        requirements = crawled_vacancy.snippet.requirement
        speciality = crawled_vacancy.speciality
        tags = crawled_vacancy.tags
        publish_timestamp = self._canonize_timestamp(crawled_vacancy.published_at)
        vacancy = Vacancy(
            canonized_url=canonized_url,
            original_url=original_url,
            api_url=api_url,
            title=title,
            area_id=area_id,
            salary=salary,
            requirements=requirements,
            speciality=speciality,
            tags=tags,
            publish_timestamp=publish_timestamp,
        )
        self.write_output(vacancy.table_record())

    def _canonize_timestamp(self, timestamp: str) -> int:
        return int(datetime.fromisoformat(timestamp).timestamp())

    def _get_area_id(self, area: APIArea) -> int:
        # TODO: convert from hh_area_id to area_id (currently they are the same)
        return area.id
