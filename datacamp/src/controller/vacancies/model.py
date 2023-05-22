import json
import validators
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field, validator
from lib.specialities import Speciality


class Salary(BaseModel):
    currency: str | None
    from_: int | None = Field(alias='from')
    gross: bool | None
    to: int | None

    class Config:
        allow_population_by_field_name = True


class Vacancy(BaseModel):
    canonized_url: str
    original_url: str
    api_url: str
    title: str
    area_id: int
    salary: Salary | None
    requirements: str | None
    speciality: str
    tags: List[str]
    publish_timestamp: int

    @validator('canonized_url')
    def is_valid_canonized_url(cls, v):
        assert validators.url(v), 'Canonized url is not valid'
        return v

    @validator('original_url')
    def is_valid_original_url(cls, v):
        assert validators.url(v), 'Original url is not valid'
        return v

    @validator('speciality')
    def is_speciality_valid(cls, v):
        assert v in Speciality.DEVELOPMENT.values(), f'Speciality is not present in Speciality enum (speciality={v})'
        return v

    # @validator('salary')
    # def is_salary_valid(cls, v):
    #     if v is not None:
    #         Salary.parse_raw(v)
    #     return v

    @validator('publish_timestamp')
    def is_valid_date(cls, v):
        assert datetime(1900, 1, 1) <= datetime.utcfromtimestamp(v) <= datetime(2100, 1, 1), 'Publish timestamp has invalid value (out of range)'
        return v


    def table_record(self) -> Dict:
        d = self.dict(by_alias=True)
        d['salary'] = json.dumps(d['salary'])
        return d


class VacancyRecord(Vacancy):
    insert_timestamp: int
    resource_name: str
    source_name: str

    def unique_key(self) -> Dict:
        return {
            'resource_name': self.resource_name,
            'source_name': self.source_name,
            'canonized_url': self.canonized_url,
        }

    @staticmethod
    def create_table_query() -> str:
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp  BIGINT,
                resource_name     VARCHAR(128) NOT NULL,
                source_name       VARCHAR(128) NOT NULL,
                canonized_url     VARCHAR(2048) NOT NULL,
                original_url      VARCHAR(2048) NOT NULL,
                api_url           VARCHAR(2048) NOT NULL,
                title             VARCHAR(256) NOT NULL,
                area_id           BIGINT NOT NULL,
                salary            JSON,
                requirements      TEXT,
                speciality        VARCHAR(256) NOT NULL,
                tags              VARCHAR(256)[] NOT NULL check (array_position(tags, null) is null),
                publish_timestamp BIGINT NOT NULL
            )
        """
