import json
import time
import traceback
from typing import Dict

from src.types.resources import ResourceName
from src.controller.base import ControllerBase
from src.controller.posts.model import PostRecord


class PostsController(ControllerBase):
    RESOURCE_NAME = ResourceName.POST

    def store(self, record: Dict) -> None:
        post_record = PostRecord(**record)
        try:
            self._store(post_record)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'unique_key': post_record.unique_key()},
            }))

    def _store(self, post_record: PostRecord) -> None:
        stored_post_record = self._get_same_stored(post_record)
        if stored_post_record is None:
            self._insert(post_record)
        else:
            self._merge(stored_post_record, post_record)

    def _get_same_stored(self, post_record: PostRecord) -> PostRecord | None:
        select_ = self.storage.select(where=post_record.unique_key())
        if len(select_) == 0:
            return
        return PostRecord(**select_[0])

    def _insert(self, post_record: PostRecord) -> None:
        post_record.insert_timestamp = int(time.time())
        self.storage.insert([post_record.dict()])

    def _merge(self, stored_post_record: PostRecord, new_post_record: PostRecord) -> None:
        new_post_record.rank = max(new_post_record.rank, stored_post_record.rank)
        new_post_record.insert_timestamp = int(time.time())
        self.storage.update(set_=new_post_record.dict(), where=new_post_record.unique_key())
