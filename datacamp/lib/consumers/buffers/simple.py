
from collections import deque
from typing import Any

from .base import BufferBase


class SimpleBuffer(BufferBase):
    BUFFER_SIZE = 100

    def __init__(self, *args, buffer_size=BUFFER_SIZE, **kwargs):
        assert buffer_size >= 0, 'Buffer size can\'t be negative'
        self._storage = deque()
        self._buffer_size = buffer_size
        super().__init__(*args, **kwargs)

    def write(self, data: Any) -> None:
        assert not self.full, 'Buffer size limit reached'
        self._storage.append(data)

    def read(self) -> Any:
        assert not self.empty
        return self._storage.popleft()

    @property
    def size(self):
        return len(self._storage)

    @property
    def empty(self):
        return self.size == 0

    @property
    def full(self):
        return self.size == self._buffer_size

class SimpleUnboundedBuffer(BufferBase):
    def __init__(self, *args, **kwargs):
        self._storage = deque()
        super().__init__(*args, **kwargs)

    def write(self, data: Any) -> None:
        self._storage.append(data)

    def read(self) -> Any:
        assert not self.empty
        return self._storage.popleft()

    @property
    def size(self):
        return len(self._storage)

    @property
    def empty(self):
        return self.size == 0

    @property
    def full(self):
        return False
