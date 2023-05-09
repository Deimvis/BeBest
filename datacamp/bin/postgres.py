import logging
import psycopg2
from psycopg2.extensions import AsIs
from lib.utils.temporary import temporary_set_attr


class PostgresConnection:
    def __init__(self, db_name=None, user=None, password=None, host=None, port=None):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


def create_database(conn: psycopg2.extensions.connection, db_name: str):
    query = """
        CREATE DATABASE %s
            ENCODING='UTF8'
            LC_COLLATE='C'
            LC_CTYPE='C'
            TEMPLATE template0
    """
    with temporary_set_attr(conn, 'autocommit', True):
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, (AsIs(db_name),))
            except psycopg2.errors.DuplicateDatabase as error:
                logging.info(f'Database {db_name} already exists')
