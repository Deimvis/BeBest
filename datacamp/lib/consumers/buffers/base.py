from abc import ABC, abstractmethod
from typing import Any, Iterable


class BufferBase(ABC):
    @abstractmethod
    def write(self, data: Any) -> None:
        pass

    @abstractmethod
    def read(self) -> Any:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @property
    @abstractmethod
    def full(self) -> bool:
        pass
