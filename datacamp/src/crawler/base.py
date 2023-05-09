import time
from abc import ABC, abstractmethod

from lib.consumers import ConsumerBased, ConsumerGate


class CrawlerBase(ConsumerBased, ConsumerGate, ABC):

    @abstractmethod
    def crawl(self) -> None:
        pass

    @property
    @abstractmethod
    def RESOURCE_NAME(self):
        pass

    @property
    @abstractmethod
    def SOURCE_NAME(self):
        pass

    def write_output(self, data: str) -> None:
        self.output_consumer.recv({
            'insert_timestamp': int(time.time()),
            'resource_name': self.RESOURCE_NAME,
            'source_name': self.SOURCE_NAME,
            'data': data,
        })
