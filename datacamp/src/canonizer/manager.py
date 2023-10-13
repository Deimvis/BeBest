from collections import defaultdict
from typing import Iterable, Type
from src.types.sources import SourceName
from src.types import ResourceName
from .base import CanonizerBase


class CanonizersManager:
    def __init__(self, Canonizers: Iterable[Type[CanonizerBase]]):
        self._Canonizers = Canonizers
        self._resource_name2source_name2Canonizer = defaultdict(dict)
        for Canonizer in Canonizers:
            self._resource_name2source_name2Canonizer[Canonizer.RESOURCE_NAME][Canonizer.SOURCE_NAME] = Canonizer

    def find_Canonizer(self, resource_name: str, source_name: str) -> Type[CanonizerBase]:
        assert resource_name in ResourceName.all()
        assert source_name in SourceName.all()
        return self.resource_name2source_name2Canonizer[resource_name][source_name]

    @property
    def Canonizers(self):
        return self._Canonizers

    @property
    def resource_name2source_name2Canonizer(self):
        return self._resource_name2source_name2Canonizer

