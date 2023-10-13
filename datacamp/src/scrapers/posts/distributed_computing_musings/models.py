from typing import List
from pydantic import BaseModel


class Article(BaseModel):
    title: str
    tags: List[str]
    publish_date: str  # Format: 'MMM DD, YYYY' (month is string)
    starting_text: str
    url: str
