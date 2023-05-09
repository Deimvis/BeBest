import json
from typing import Dict

from .base import ConsumerBase


class FileConsumer(ConsumerBase):
    def __init__(self, *args, file_path: str = None,  **kwargs):
        assert file_path is not None, 'File is not specified for FileConsumer'
        self._file_path = file_path
        super().__init__(*args, **kwargs)

    def recv(self, data: Dict) -> None:
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False) + '\n\n')

    def on_start(self):
        pass

    def on_finish(self):
        pass

    @property
    def file_path(self):
        return self._file_path
