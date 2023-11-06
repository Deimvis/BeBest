from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator


class Article(BaseModel):
    author_username: str | None
    publish_date: str
    starting_text: str
    tags: List[str]
    title: str
    url: str

    @field_validator('publish_date')
    @classmethod
    def is_valid_publish_date(cls, v):
        assert datetime.strptime(v, '%Y/%m/%d'), f'Publish date {v} has wrong format ("%Y/%m/%d" is expected)'
        return v
