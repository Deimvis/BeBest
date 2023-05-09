from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    code: str
    source_name: str
    note: Optional[str]
