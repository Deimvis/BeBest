from pydantic import BaseModel
from typing import Optional


class Resource(BaseModel):
    code: str
    resource_name: str
    note: Optional[str]
