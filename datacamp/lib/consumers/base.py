from abc import ABC, abstractmethod
from typing import Dict, Iterable


class ConsumerBase(ABC):

    @abstractmethod
    def recv(self, data: Dict) -> None:
        pass

    def recv_many(self, data_seq: Iterable[Dict]) -> None:
        for data in data_seq:
            self.recv(data)

    def on_start(self):
        if hasattr(super(), 'on_start'):
            super(self).on_start()

    def on_finish(self):
        if hasattr(super(), 'on_finish'):
            super().on_finish()

    def __enter__(self):
        self.on_start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.on_finish()
