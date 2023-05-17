import contextlib
import logging
import psycopg2
import psycopg2.extras
from collections import defaultdict
from psycopg2.extensions import AsIs
from typing import Any, Dict, List, Sequence, Tuple

import lib.utils as utils


log_ = logging.getLogger(__name__)


class PostgresAPI:
    def __init__(self, connection: psycopg2.extensions.connection):
        self._connection = connection

    def execute(self, query, vars_=None, cursor=None) -> Any:
        with contextlib.ExitStack() as stack:
            if cursor is None:
                cursor = stack.enter_context(self.connection.cursor())
            return cursor.execute(query, vars_)

    @utils.logging.logging_on_call('Create table `{table_name}`', logging.DEBUG, logger=log_)
    def create_table(self, table_name: str, query: str) -> None:
        self.execute(query, (AsIs(table_name),))

    @utils.logging.logging_on_call('Truncate table `{table_name}`', logging.DEBUG, logger=log_)
    def truncate_table(self, table_name: str) -> None:
        self.execute('TRUNCATE TABLE %s', (AsIs(table_name),))

    @utils.logging.logging_on_call('Drop table `{table_name}`', logging.DEBUG, logger=log_)
    def drop_table(self, table_name: str) -> None:
        self.execute('DROP TABLE IF EXISTS %s', (AsIs(table_name),))

    @utils.logging.logging_on_call('Table exists `{table_name}`', logging.DEBUG, logger=log_)
    def table_exists(self, table_name: str) -> bool:
        with self.connection.cursor() as cursor:
            self.execute('SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = \'public\' AND tablename = %s)', (table_name,), cursor=cursor)
            return cursor.fetchone()[0]

    @utils.logging.logging_on_call('Select table `{table_name}`', logging.DEBUG, logger=log_)
    def select(self, table_name: str, where: Dict = None, cursor_kwargs={'cursor_factory': psycopg2.extras.DictCursor}) -> List[Any]:
        with self.connection.cursor(**cursor_kwargs) as cursor:
            query = 'SELECT * FROM %s'
            vars_ = [AsIs(table_name)]
            if where is not None:
                where_statement, where_vars = self._format_where(where)
                query = query + ' ' + where_statement
                vars_ = vars_ + where_vars
            self.execute(query, vars_, cursor=cursor)
            return cursor.fetchall()

    @utils.logging.logging_on_call('Exists `{table_name}` where {where}', logging.DEBUG, logger=log_)
    def exists(self, table_name: str, where: Dict) -> bool:
        # select exists(select 1 from contact where id=12)
        raise NotImplementedError()

    @utils.logging.logging_on_call('Insert {row_count} rows in `{table_name}`', logging.DEBUG, logger=log_, row_count=lambda **func_args: len(func_args['rows']))
    def insert(self, table_name: str, rows: Sequence[Dict]) -> None:
        row_groups = defaultdict(list)
        for row in rows:
            columns = tuple(sorted(row.keys()))
            values = tuple(v for _, v in sorted(row.items(), key=lambda item: item[0]))
            row_groups[columns].append(values)

        with self.connection.cursor() as cursor:
            for columns, values_list in row_groups.items():
                utils.postgres.insert_many(cursor, table_name, values_list, columns=columns)

    @utils.logging.logging_on_call('Update `{table_name}`', logging.DEBUG, logger=log_)
    def update(self, table_name: str, set_: Dict, where: Dict):
        query = 'UPDATE %s'
        vars_ = [AsIs(table_name)]
        set_statement, set_vars = self._format_set(set_)
        where_statement, where_vars = self._format_where(where)
        query = f'{query} {set_statement} {where_statement}'
        vars_ = vars_ + set_vars + where_vars
        self.execute(query, vars_)

    @utils.logging.logging_on_call('Row count table `{table_name}`', logging.DEBUG, logger=log_)
    def row_count(self, table_name: str) -> int:
        with self.connection.cursor() as cursor:
            self.execute('SELECT COUNT(*) FROM %s', (AsIs(table_name),), cursor=cursor)
            return cursor.fetchone()[0]

    @utils.logging.logging_on_call('Rename table `{table_name}`', logging.DEBUG, logger=log_)
    def rename_table(self, table_name: str, dst_table_name: str) -> None:
        self.execute('ALTER TABLE IF EXISTS %s RENAME TO %s', (AsIs(table_name), AsIs(dst_table_name),))

    @utils.logging.logging_on_call('Commit', logging.DEBUG, logger=log_)
    def commit(self) -> None:
        self.connection.commit()

    @staticmethod
    def _format_where(where: dict) -> Tuple[str, List]:
        # https://docs.python.org/3.7/library/stdtypes.html#typesmapping:
        # "Changed in version 3.7: Dictionary order is guaranteed to be insertion order"
        statement = 'WHERE ' + ' AND '.join(f'{col_name} = %s' for col_name in where.keys())
        return statement, list(where.values())

    @staticmethod
    def _format_set(set_: dict) -> Tuple[str, List]:
        # https://docs.python.org/3.7/library/stdtypes.html#typesmapping:
        # "Changed in version 3.7: Dictionary order is guaranteed to be insertion order"
        statement = 'SET ' + ', '.join(f'{col_name} = %s' for col_name in set_.keys())
        return statement, list(set_.values())

    @property
    def connection(self):
        return self._connection
