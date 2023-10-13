from pydantic import BaseModel
from typing import List
from src.scrapers.plan_base import ScrapePlanBase



class HabrPostsScrapePlan(ScrapePlanBase):
    class Hub(BaseModel):
        url: str
        hubs: List[str] | None = None

    hubs: List[Hub]
