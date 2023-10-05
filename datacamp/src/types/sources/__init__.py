import json
import os
from pathlib import Path
from typing import Set
from lib.utils.enum import SimpleEnum

from .model import Source


with (Path(os.getenv('FILES_DIR_PATH')) / 'sources.json').open('r') as f:
    SOURCES = json.load(f)


class SourceNameType(type):
    def __new__(metacls, cls, bases, classdict):
        for v in SOURCES:
            source = Source.parse_obj(v)
            classdict[source.code] = source.source_name
        return super().__new__(metacls, cls, bases, classdict)


class SourceName(SimpleEnum, metaclass=SourceNameType):
    """
    SourceName is enum representation of source names,
    so SourceName.<SOURCE_NAME> == <SOURCE_NAME>.
    Source names are stored in resource (SOURCE_NAMES_RESOURCE_NAME).
    """

    @classmethod
    def all(cls) -> Set[str]:
        """ Return set of all source names """
        return SourceName.values()
