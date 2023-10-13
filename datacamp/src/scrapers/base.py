import time
from typing import Type
from abc import ABC, abstractmethod

from lib.consumers import ConsumerBased, ConsumerGate
from .plan_base import ScrapePlanBase


class ScraperBase(ConsumerBased, ConsumerGate, ABC):

    @abstractmethod
    def scrape(self, plan: ScrapePlanBase) -> None:
        pass

    @property
    @abstractmethod
    def RESOURCE_NAME(self) -> str:
        pass

    @property
    @abstractmethod
    def SOURCE_NAME(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def plan_type(cls) -> Type[ScrapePlanBase]:
        return ScrapePlanBase

    def write_output(self, data: str) -> None:
        self.output_consumer.recv({
            'insert_timestamp': int(time.time()),
            'resource_name': self.RESOURCE_NAME,
            'source_name': self.SOURCE_NAME,
            'data': data,
        })
