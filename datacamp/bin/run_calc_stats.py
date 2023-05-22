import os
from psycopg2.extensions import AsIs
from bin.postgres import PostgresConnection
from lib.consumers import PostgresConsumer
from lib.storages.postgres.table import PostgresTable


class StatsCalculatorLogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def storage_create_table_query():
    return """
        CREATE TABLE IF NOT EXISTS %s (
            source_name       VARCHAR(128) NOT NULL,
            area_id           BIGINT NOT NULL,
            speciality        VARCHAR(256) NOT NULL,
            tags              VARCHAR(256)[] NOT NULL check (array_position(tags, null) is null),
            salary            JSON
        )
    """


def run_calc_stats(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:

        storage = PostgresTable(conn, args.storage)
        storage.drop()
        storage.create(storage_create_table_query())
        storage.commit()

        calc_stats_query = """
            INSERT INTO %s
            SELECT
                source_name,
                area_id,
                speciality,
                tags,
                salary
            FROM %s
            WHERE salary::text != 'null'
                AND CAST(salary AS json)->>'currency' != 'null'
                AND (extract(epoch from now())::INT - publish_timestamp) < 360 * 24 * 3600  -- PUBLISHED NO EARLIER THAN YEAR AGO
        """
        storage.api.execute(calc_stats_query, (AsIs(storage.table_name), AsIs(args.vacancies)))
        storage.api.commit()
