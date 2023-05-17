import psycopg2
from typing import Any, Dict, List, Sequence

from .api import PostgresAPI
from lib.storages.base import StorageBase


class PostgresTable(StorageBase):
    def __init__(self, connection: psycopg2.extensions.connection, table_name: str):
        self._api = PostgresAPI(connection)
        self._table_name = table_name

    def create(self, query: str) -> None:
        self.api.create_table(self.table_name, query)

    def exists(self) -> bool:
        return self.api.table_exists(self.table_name)

    def truncate(self) -> None:
        self.api.truncate_table(self.table_name)

    def drop(self) -> None:
        self.api.drop_table(self.table_name)

    def has(self, where: Dict = None) -> bool:
        return self.api.exists(self.table_name, where=where)

    def select(self, where: Dict = None) -> List[Any]:
        return self.api.select(self.table_name, where=where)

    def insert(self, rows: Sequence[Dict]) -> None:
        self.api.insert(self.table_name, rows)

    def update(self, set_: Dict, where: Dict) -> None:
        self.api.update(self.table_name, set_=set_, where=where)

    def row_count(self) -> int:
        return self.api.row_count(self.table_name)

    def move(self, dst_table_name: str) -> None:
        self.api.drop_table(dst_table_name)
        self.api.rename_table(self.table_name, dst_table_name)

    def commit(self) -> None:
        self.api.commit()

    @property
    def api(self) -> PostgresAPI:
        return self._api

    @property
    def table_name(self) -> str:
        return self._table_name
