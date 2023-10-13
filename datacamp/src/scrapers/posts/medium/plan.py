from pydantic import BaseModel
from typing import List
from src.scrapers.plan_base import ScrapePlanBase

class MediumPostsScrapePlan(ScrapePlanBase):
    class Blog(BaseModel):
        url: str
        author_username: str | None = None
        publsher: str | None = None

    blogs: List[Blog]
