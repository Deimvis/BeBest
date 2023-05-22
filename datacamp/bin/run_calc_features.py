import os
from psycopg2.extensions import AsIs
from bin.postgres import PostgresConnection
from lib.consumers import PostgresConsumer
from lib.storages.postgres.table import PostgresTable


class FeaturesCalculatorLogsConsumer(PostgresConsumer):

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
            update_timestamp   BIGINT,
            post_canonized_url VARCHAR(2048) UNIQUE NOT NULL,
            clicks_count       BIGINT
        )
    """


def run_calc_features(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:

        storage = PostgresTable(conn, args.storage)
        storage.create_if_not_exists(storage_create_table_query())
        storage.commit()
        storage.truncate()
        storage.commit()

        calc_features_query = """
            WITH recent_redirects AS (
                SELECT
                    CAST(CAST(action_value AS JSON)->'redirect_to' AS VARCHAR(2048)) AS redirect_url
                FROM log_proxy_userlog
                WHERE "action" = 'go_to'
                    AND TIMESTAMP > extract(epoch from now())::bigint - 7 * 24 * 3600
            )
            INSERT INTO %s
            SELECT
                extract(epoch from now())::bigint AS update_timestamp,
                redirect_url AS post_canonized_url,
                COUNT(*) AS clicks_count
            FROM recent_redirects
            WHERE redirect_url != 'null'
            GROUP BY redirect_url
            ORDER BY post_canonized_url
        """
        storage.api.execute(calc_features_query, (AsIs(storage.table_name),))
        storage.api.commit()
