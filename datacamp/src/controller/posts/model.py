import validators
from datetime import datetime
from pydantic import BaseModel, validator
from typing import Dict, List
from lib.specialities import Speciality


class RawPost(BaseModel):
    canonized_url: str
    original_url: str
    title: str
    topics: List[str]
    starting_text: str
    publish_timestamp: int
    author_username: str | None
    views: int | None

    @validator('canonized_url')
    def is_valid_canonized_url(cls, v):
        assert validators.url(v), 'Canonized url is not valid'
        return v

    @validator('original_url')
    def is_valid_original_url(cls, v):
        assert validators.url(v), 'Original url is not valid'
        return v

    @validator('topics')
    def are_topics_valid(cls, v):
        for topic in v:
            assert topic in Speciality.DEVELOPMENT.values(), f'Topic is not present in Speciality enum (topic={topic})'
        return v

    @validator('publish_timestamp')
    def is_valid_date(cls, v):
        assert datetime(1900, 1, 1) <= datetime.utcfromtimestamp(v) <= datetime(2100, 1, 1), 'Publish timestamp has invalid value (out of range)'
        return v


class Post(RawPost):
    rank: int

    @validator('rank')
    def is_rank_valid(cls, v):
        assert v >= 0, 'Rank is not valid (out of range)'
        return v


class PostRecord(Post):
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
                title             VARCHAR(256) NOT NULL,
                topics            VARCHAR(256)[] NOT NULL check (array_position(topics, null) is null),
                rank              BIGINT NOT NULL,
                starting_text     TEXT NOT NULL,
                publish_timestamp BIGINT NOT NULL,
                author_username   VARCHAR(128),
                views             BIGINT
            )
        """
