import json
import os
from pathlib import Path
from typing import Dict, List, Set
from lib.utils.enum import SimpleEnum

from .model import Resource


RESOURCES_FILE: Path = Path(os.getenv('FILES_DIR_PATH')) / 'resources.json'
assert RESOURCES_FILE.exists(), f'Resources file is not found in FILES_DIR_PATH ({RESOURCES_FILE.absolute()} does not exist)'
RESOURCES: List[Dict] = json.loads(RESOURCES_FILE.read_text())


class ResourceNameType(type):
    def __new__(metacls, cls, bases, classdict):
        for v in RESOURCES:
            source = Resource.model_validate(v)
            classdict[source.code] = source.resource_name
        return super().__new__(metacls, cls, bases, classdict)


class ErrorOnAccessDescriptor:
    def __get__(self, instance, owner):
        raise AttributeError('Access to this attribute is not allowed.')


class ResourceName(SimpleEnum, metaclass=ResourceNameType):
    """
    SourceName is enum representation of source names,
    so SourceName.<RESOURCE_CODE> == <RESOURCE_NAME>.
    Source names are stored in resource (SOURCE_NAMES_RESOURCE_NAME).
    """
    POST = ErrorOnAccessDescriptor()
    VACANCY = ErrorOnAccessDescriptor()

    @classmethod
    def all(cls) -> Set[str]:
        """ Return set of all source names """
        return ResourceName.values()
