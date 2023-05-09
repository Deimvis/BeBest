import time
from abc import ABC, abstractmethod
from typing import Dict

from lib.consumers import LogsConsumerBased, LogsConsumerGate
from lib.storages import StorageBased


class ControllerBase(StorageBased, LogsConsumerBased, LogsConsumerGate, ABC):

    @abstractmethod
    def store(self, record: Dict) -> None:
        pass

    @property
    @abstractmethod
    def RESOURCE_NAME(self):
        pass

    def write_output(self, data: Dict) -> None:
        common = {
            'insert_timestamp': int(time.time()),
            'resource_name': self.RESOURCE_NAME,
        }
        self.output_consumer.recv(common | data)
