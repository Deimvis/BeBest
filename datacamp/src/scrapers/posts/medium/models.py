from typing import List
from pydantic import BaseModel


class Article(BaseModel):
    author_username: str
    publisher: str | None
    title: str
    tags: List[str]
    publish_date: str  # Format: 'MMM DD, YYYY' (month is string)
    url: str
