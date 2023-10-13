import json
import os
from pathlib import Path
from typing import Dict, List, Set
from lib.utils.enum import SimpleEnum

from .model import Source


SOURCES_FILE: Path = Path(os.getenv('FILES_DIR_PATH')) / 'sources.json'
assert SOURCES_FILE.exists(), f'Sources file is not found in FILES_DIR_PATH ({SOURCES_FILE.absolute()} does not exist)'
SOURCES: List[Dict] = json.loads(SOURCES_FILE.read_text())


class SourceNameType(type):
    def __new__(metacls, cls, bases, classdict):
        for v in SOURCES:
            source = Source.model_validate(v)
            classdict[source.code] = source.source_name
        return super().__new__(metacls, cls, bases, classdict)


class ErrorOnAccessDescriptor:
    def __get__(self, instance, owner):
        raise AttributeError('Access to this attribute is not allowed.')


class SourceName(SimpleEnum, metaclass=SourceNameType):
    """
    SourceName is enum representation of source names,
    so SourceName.<SOURCE_CODE> == <SOURCE_NAME>.
    Source names are stored in resource (SOURCE_NAMES_RESOURCE_NAME).
    """
    HABR = ErrorOnAccessDescriptor()
    MEDIUM = ErrorOnAccessDescriptor()
    DCM = ErrorOnAccessDescriptor()
    HH_API = ErrorOnAccessDescriptor()

    @classmethod
    def all(cls) -> Set[str]:
        """ Return set of all source names """
        return SourceName.values()
