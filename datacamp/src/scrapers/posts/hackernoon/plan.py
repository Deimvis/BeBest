import re
from pydantic import BaseModel, field_validator
from typing import List
from src.scrapers.plan_base import ScrapePlanBase


class HackernoonPostsScrapePlan(ScrapePlanBase):
    class Tag(BaseModel):
        name: str
        page_count: int = 5

        @property
        def url(self):
            return f'https://hackernoon.com/tagged/{self.name}'

    tags: List[Tag]
