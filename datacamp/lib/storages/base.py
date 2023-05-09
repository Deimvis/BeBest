from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence


class StorageBase(ABC):

    @abstractmethod
    def create(self, query: str) -> None:
        pass

    @abstractmethod
    def exists(self) -> bool:
        pass

    @abstractmethod
    def truncate(self) -> None:
        pass

    @abstractmethod
    def has(self, where: Dict = None) -> bool:
        pass

    @abstractmethod
    def select(self, where: Dict = None) -> List[Any]:
        pass

    @abstractmethod
    def insert(self, rows: Sequence[Dict]) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    def create_if_not_exists(self, create_query: str) -> None:
        if not self.exists():
            self.create(create_query)
