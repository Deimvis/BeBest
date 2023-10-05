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
            query = 'SELECT * FROM "%s"'
            vars_ = [AsIs(table_name)]
            if where is not None:
                where_statement, where_vars = self._format_where(where)
                query = query + ' ' + where_statement
                vars_ = vars_ + where_vars
            self.execute(query, vars_, cursor=cursor)
            return cursor.fetchall()

    @utils.logging.logging_on_call('Exists `{table_name}` where {where}', logging.DEBUG, logger=log_)
    def exists(self, table_name: str, where: Dict) -> bool:
        with self.connection.cursor() as cursor:
            query = 'SELECT EXISTS (SELECT 1 FROM "%s"'
            vars_ = [AsIs(table_name)]
            where_statement, where_vars = self._format_where(where)
            query = query + ' ' + where_statement + ')'
            vars_ = vars_ + where_vars
            self.execute(query, vars_, cursor=cursor)
            return cursor.fetchone()[0]

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

    @utils.logging.logging_on_call('Insert (v2) {row_count} rows in `{table_name}`', logging.DEBUG, logger=log_, row_count=lambda **func_args: len(func_args['rows']))
    def insert_v2(self,  table_name: str, rows: Sequence[Dict], conflict_columns: Sequence[str] = None, conflict_set: Sequence[str] = None, conflict_do_nothing: bool = False):
        row_groups = defaultdict(list)
        for row in rows:
            columns = tuple(sorted(row.keys()))
            values = tuple(v for _, v in sorted(row.items(), key=lambda item: item[0]))
            row_groups[columns].append(values)

        with self.connection.cursor() as cursor:
            for columns, values_list in row_groups.items():
                self._insert_many(table_name, columns, values_list, conflict_columns, conflict_set, conflict_do_nothing)

    def _insert_many(self, table_name: str, columns: Sequence[str], values_seq: Sequence[Tuple], conflict_columns: Sequence[str] = None, conflict_set: Sequence[str] = None, conflict_do_nothing: bool = False) -> None:
        # NOTE: NOT TESTED PROPERLY
        if len(values_seq) == 0:
            return
        with self.connection.cursor() as cursor:
            values_format = '(' + ','.join(['%s' for _ in range(len(values_seq[0]))]) + ')'
            values_str = ','.join(cursor.mogrify(values_format, values).decode('utf-8') for values in values_seq)
            query = ''.join([
                'INSERT INTO ',
                f'"{table_name}" ',
                f'({",".join(columns)}) ' if columns is not None else '',
                'VALUES ',
                f'{values_str} ',
                self._format_conflict(conflict_columns, conflict_set or columns, conflict_do_nothing) if conflict_columns is not None else ''
            ])
            cursor.execute(query)

    @utils.logging.logging_on_call('Update `{table_name}`', logging.DEBUG, logger=log_)
    def update(self, table_name: str, set_: Dict, where: Dict):
        query = 'UPDATE %s'
        vars_ = [AsIs(table_name)]
        set_statement, set_vars = self._format_set(set_)
        where_statement, where_vars = self._format_where(where)
        query = f'{query} {set_statement} {where_statement}'
        vars_ = vars_ + set_vars + where_vars
        self.execute(query, vars_)

    @utils.logging.logging_on_call('Count table `{table_name}`', logging.DEBUG, logger=log_)
    def count(self, table_name: str, where: Dict = None) -> int:
        with self.connection.cursor() as cursor:
            query = 'SELECT COUNT(*) FROM "%s"'
            vars_ = [AsIs(table_name)]
            if where is not None:
                where_statement, where_vars = self._format_where(where)
                query = query + ' ' + where_statement
                vars_ = vars_ + where_vars
            self.execute(query, vars_, cursor=cursor)
            return cursor.fetchone()[0]

    @utils.logging.logging_on_call('Row count table `{table_name}`', logging.DEBUG, logger=log_)
    def row_count(self, table_name: str) -> int:
        # TODO: depr, replace with `count`
        return self.count(table_name)

    def delete(self, table_name: str, where: Dict=None) -> None:
        query = 'DELETE FROM "%s"'
        vars_ = [AsIs(table_name)]
        if where is not None:
            where_statement, where_vars = self._format_where(where)
            query = query + ' ' + where_statement
            vars_ = vars_ + where_vars
        self.execute(query, vars_)

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

    @staticmethod
    def _format_conflict(conflict_columns: Sequence[str], conflict_set: Sequence[str] | None, conflict_do_nothing: bool) -> Tuple[str, List]:
        # NOTE: NOT TESTED PROPERLY
        return ''.join([
            'ON CONFLICT ',
            '(' + ','.join(conflict_columns) + ') ',
            'DO UPDATE SET ' + ','.join(f'{col_name} = excluded.{col_name}' for col_name in conflict_set) if not conflict_do_nothing else 'DO NOTHING',
        ])

    @property
    def connection(self):
        return self._connection
