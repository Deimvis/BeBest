import json
import os
from pathlib import Path
from typing import Set
from lib.utils.enum import SimpleEnum

from .model import Resource


with (Path(os.getenv('FILES_DIR_PATH')) / 'resources.json').open('r') as f:
    RESOURCES = json.load(f)


class ResourceNameType(type):
    def __new__(metacls, cls, bases, classdict):
        for v in RESOURCES:
            source = Resource.parse_obj(v)
            classdict[source.code] = source.resource_name
        return super().__new__(metacls, cls, bases, classdict)


class ResourceName(SimpleEnum, metaclass=ResourceNameType):
    """
    SourceName is enum representation of source names,
    so SourceName.<SOURCE_NAME> == <SOURCE_NAME>.
    Source names are stored in resource (SOURCE_NAMES_RESOURCE_NAME).
    """

    @classmethod
    def all(cls) -> Set[str]:
        """ Return set of all source names """
        return ResourceName.values()
