from src.types import ResourceName
from src.controller.posts.models import PostRecord
from src.controller.vacancies.model import VacancyRecord


def find_create_table_query(resource_name):
    match resource_name:
        case ResourceName.POST:
            return PostRecord.create_table_query()
        case ResourceName.VACANCY:
            return VacancyRecord.create_table_query()
        case _:
            raise RuntimeError(f'Couldn\'t find corresponding create table query for resource name: {resource_name}')
