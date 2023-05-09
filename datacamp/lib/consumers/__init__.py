from .base import ConsumerBase  # noqa
from .buffered import BufferedConsumer  # noqa
from .dishonest import DishonestConsumer  # noqa
from .file import FileConsumer  # noqa
from .postgres import PostgresConsumer  # noqa

import logging
import time
from abc import ABC, abstractmethod


class ConsumerBased:
    def __init__(self, *args, output_consumer: ConsumerBase = None, logs_consumer: ConsumerBase = None, **kwargs):
        assert output_consumer is not None, 'Output consumer isn\'t specified'
        assert logs_consumer is not None, 'Logs consumer isn\'t specified'
        self._output_consumer = output_consumer
        self._logs_consumer = logs_consumer
        super().__init__(*args, **kwargs)

    @property
    def output_consumer(self):
        return self._output_consumer

    @property
    def logs_consumer(self):
        return self._logs_consumer


class ConsumerGate(ABC):

    @abstractmethod
    def write_output(self, data: str) -> None:
        pass

    def write_log(self, level: int, msg: str) -> None:
        self.logs_consumer.recv({
            'insert_timestamp': int(time.time()),
            'level': logging.getLevelName(level),
            'msg': msg,
        })

    def write_error(self, msg: str) -> None:
        self.write_log(logging.ERROR, msg)


class LogsConsumerBased:
    def __init__(self, *args, logs_consumer: ConsumerBase = None, **kwargs):
        assert logs_consumer is not None, 'Logs consumer isn\'t specified'
        self._logs_consumer = logs_consumer
        super().__init__(*args, **kwargs)

    @property
    def output_consumer(self):
        return self._output_consumer

    @property
    def logs_consumer(self):
        return self._logs_consumer


class LogsConsumerGate(ABC):
    def write_log(self, level: int, msg: str) -> None:
        self.logs_consumer.recv({
            'insert_timestamp': int(time.time()),
            'level': logging.getLevelName(level),
            'msg': msg,
        })

    def write_error(self, msg: str) -> None:
        self.write_log(logging.ERROR, msg)
