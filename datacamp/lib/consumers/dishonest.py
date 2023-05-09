from typing import Callable, Dict, Iterable

from .base import ConsumerBase


class DishonestConsumer(ConsumerBase):
    def __init__(self, *args, data_modifier: Callable[[Dict], Dict | Iterable[Dict]] = lambda x: x, **kwargs):
        self._data_modifier = data_modifier
        super().__init__(*args, **kwargs)

    def recv(self, data: Dict) -> None:
        modified_data = self.data_modifier(data)
        match modified_data:
            case dict():
                super().recv(modified_data)
            case _:
                for item in modified_data:
                    super().recv(item)

    def on_start(self):
        return super().on_start()

    def on_finish(self):
        return super().on_finish()

    @property
    def data_modifier(self):
        return self._data_modifier
