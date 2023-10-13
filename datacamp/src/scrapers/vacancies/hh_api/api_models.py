from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


NOT_USED = Any | None


class Area(BaseModel):
    id: str
    name: str
    url: str


class ProfessionalRole(BaseModel):
    id: str
    name: str


class Salary(BaseModel):
    currency: str | None
    from_: int | None = Field(alias='from')
    gross: bool | None
    to: int | None

    class Config:
        populate_by_name = True


class VacancyType(BaseModel):
    id: str
    name: str


class Snippet(BaseModel):
    requirement: str | None
    responsibility: str | None


class Vacancy(BaseModel):
    accept_incomplete_resumes: bool
    accept_temporary: bool | None
    address: NOT_USED
    adv_response_url: str | None
    alternate_url: str
    apply_alternate_url: str
    archived: bool | None
    area: Area
    contacts: NOT_USED
    created_at: str | None
    department: NOT_USED
    employer: NOT_USED
    has_test: bool
    id: str
    insider_interview: NOT_USED
    metro_stations: NOT_USED
    name: str
    premium: bool | None
    professional_roles: List[ProfessionalRole]
    published_at: str
    relations: NOT_USED
    response_letter_required: bool
    response_url: str | None
    salary: Salary | None
    schedule: NOT_USED
    sort_point_distance: int | None
    type: VacancyType
    url: str
    working_days: NOT_USED
    working_time_intervals: NOT_USED
    working_time_modes: NOT_USED
    counters: NOT_USED
    employment: NOT_USED
    experience: NOT_USED
    snippet: Snippet


class VacanciesResponse(BaseModel):
    items: List[Vacancy]
    found: int
    page: int
    pages: int
    per_page: int
    clusters: NOT_USED
    arguments: NOT_USED
    alternate_url: NOT_USED
