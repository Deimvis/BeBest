from lib.resources import ResourceName
from src.controller.posts.model import PostRecord


def find_create_table_query(resource_name):
    match resource_name:
        case ResourceName.POST:
            return PostRecord.create_table_query()
        case _:
            raise RuntimeError(f'Couldn\'t find corresponding create table query for resource name: {resource_name}')
