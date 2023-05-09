import os
import bin.helpers as helpers
from bin.postgres import PostgresConnection
from lib.consumers import PostgresConsumer
from lib.storages.postgres.table import PostgresTable
from src.controller import controllers_manager


class ControllerLogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def run_store(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:

        storage = PostgresTable(conn, args.storage)
        create_table_query = helpers.find_create_table_query(args.resource_name)
        storage.create_if_not_exists(create_table_query)
        storage.commit()

        with ControllerLogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:
            Controller = controllers_manager.find_Controller(args.resource_name)
            controller = Controller(storage=storage, logs_consumer=logs_consumer)

            input_table = PostgresTable(conn, args.input)
            for row in input_table.select():
                controller.store(row)
