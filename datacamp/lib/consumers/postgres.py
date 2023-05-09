
import psycopg2
from typing import Dict, Optional, Sequence

from .base import ConsumerBase
from lib.storages.postgres.table import PostgresTable


class PostgresConsumer(ConsumerBase):
    def __init__(self, *args,
                 connection: psycopg2.extensions.connection = None,
                 table_name = None,
                 autocommit=False,
                 truncate=False,
                 **kwargs):
        connection.autocommit = autocommit
        self._storage = PostgresTable(connection, table_name)
        self._truncate = truncate
        super().__init__(*args, **kwargs)

    def on_start(self):
        if self._truncate:
            self.storage.truncate()
        if self.create_table_query is not None:
            self.storage.create(self.create_table_query)
        super().on_start()

    def on_finish(self):
        self.storage.commit()
        super().on_finish()

    def recv(self, data: Dict) -> None:
        self.storage.insert([data])

    def recv_many(self, data_seq: Sequence[Dict]) -> None:
        self.storage.insert(data_seq)

    @property
    def storage(self) -> PostgresTable:
        return self._storage

    @property
    def create_table_query(self) -> Optional[str]:
        pass
