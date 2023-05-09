import time
from abc import ABC, abstractmethod
from typing import Dict

from lib.consumers import ConsumerBased, ConsumerGate


class CanonizerBase(ConsumerBased, ConsumerGate, ABC):

    @abstractmethod
    def canonize(self, data: str) -> None:
        pass

    @property
    @abstractmethod
    def RESOURCE_NAME(self):
        pass

    @property
    @abstractmethod
    def SOURCE_NAME(self):
        pass

    def write_output(self, data: Dict) -> None:
        common = {
            'insert_timestamp': int(time.time()),
            'resource_name': self.RESOURCE_NAME,
            'source_name': self.SOURCE_NAME,
        }
        self.output_consumer.recv(common | data)
