from typing import Dict
from enum import Enum

from .base import ConsumerBase
from .buffers.simple import SimpleBuffer, SimpleUnboundedBuffer


class BufferedConsumer(ConsumerBase):
    """
    BufferedConsumer stores received data in buffer.
    In case buffer_size == -1 (by default), it uses unbounded buffer underneath.
    It means that there is no limit on buffer size.
    """

    class OverflowMode(Enum):
        VOID = 'void'
        PARENT_CLASS = 'parent_class'

    def __init__(self, *args, buffer_size: int = -1, overflow_mode: OverflowMode = OverflowMode.VOID, flush_all_on_overflow=True, **kwargs):
        assert buffer_size >= -1, 'Buffer size should be either -1 (unbounded buffer) or non-negative number'
        if buffer_size == -1:
            self._buffer = SimpleUnboundedBuffer()
        else:
            self._buffer = SimpleBuffer(buffer_size=buffer_size)
        assert isinstance(overflow_mode, BufferedConsumer.OverflowMode), 'Overflow mode should be an instance of BufferedConsumer.OverflowMode enum'
        self._overflow_mode = overflow_mode
        self._flush_all_on_overflow = flush_all_on_overflow
        super().__init__(*args, **kwargs)

    def on_finish(self):
        self.flush_all()

    def recv(self, data: Dict) -> None:
        if self.buffer.full:
            if self._flush_all_on_overflow:
                self.flush_all()
            else:
                self.flush_one()
        self.buffer.write(data)

    def flush(self, n: int):
        values = []
        for _ in range(n):
            assert not self.buffer.empty
            values.append(self.buffer.read())

        match self.overflow_mode:
            case BufferedConsumer.OverflowMode.VOID:
                pass
            case BufferedConsumer.OverflowMode.PARENT_CLASS:
                super().recv_many(values)

    def flush_one(self):
        return self.flush(1)

    def flush_all(self):
        return self.flush(self.buffer.size)

    @property
    def buffer(self):
        return self._buffer

    @property
    def overflow_mode(self):
        return self._overflow_mode
