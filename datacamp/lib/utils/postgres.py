import psycopg2
from typing import Sequence, Tuple


def insert_many(cursor: psycopg2.extensions.cursor, table_name: str, rows: Sequence[Tuple], columns: Sequence[str] = None) -> bool:
    if len(rows) == 0:
        return False
    values_format = '(' + ','.join(['%s' for _ in range(len(rows[0]))]) + ')'
    values_str = ','.join(cursor.mogrify(values_format, row).decode('utf-8') for row in rows)
    query = ''.join([
        'INSERT INTO ',
        f'{table_name} ',
        f'({",".join(columns)}) ' if columns is not None else '',
        'VALUES ',
        values_str,
    ])
    cursor.execute(query)
    return True
