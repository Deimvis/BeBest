import os
import bin.helpers as helpers
from bin.postgres import PostgresConnection
from lib.consumers import BufferedConsumer, PostgresConsumer
from lib.storages.postgres.table import PostgresTable
from src.canonizer import canonizers_manager


class CanonizerOutputConsumer(BufferedConsumer, PostgresConsumer):
    def __init__(self, resource_name, *args, **kwargs):
        self._create_table_query = helpers.find_create_table_query(resource_name)
        super().__init__(*args, **kwargs)

    @property
    def create_table_query(self):
        return self._create_table_query


class CanonizerLogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def run_canonizer(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:
        with CanonizerOutputConsumer(args.resource_name, connection=conn, table_name=args.output, autocommit=True, truncate=True,
                                 buffer_size=10, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as output_consumer, \
                CanonizerLogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:

            Canonizer = canonizers_manager.find_Canonizer(args.resource_name, args.source_name)
            canonizer = Canonizer(output_consumer=output_consumer, logs_consumer=logs_consumer)
            # output_consumer = FileConsumer('out/out.txt')
            # logs_consumer = FileConsumer(file_path='out/logs.txt')

            input_table = PostgresTable(conn, args.input)
            for row in input_table.select():
                canonizer.canonize(row['data'])
