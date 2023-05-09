from . import (  # noqa
    base,
    postgres,
)
from .base import StorageBase  # noqa


class StorageBased:
    def __init__(self, *args, storage: StorageBase = None, **kwargs):
        assert storage is not None
        self._storage = storage
        super().__init__(*args, **kwargs)

    @property
    def storage(self) -> StorageBase:
        return self._storage
