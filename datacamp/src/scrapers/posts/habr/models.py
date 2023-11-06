from typing import List, Optional
from pydantic import BaseModel


class Article(BaseModel):
    author_username: Optional[str]
    complexity: Optional[str]
    hubs: List[str]
    reading_time: str
    starting_text: str
    tags: List[str]
    title: str
    publish_datetime: str
    url: str
    views: str
