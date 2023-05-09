import os
from bin.postgres import PostgresConnection
from lib.consumers import BufferedConsumer, PostgresConsumer
from src.crawler import crawlers_manager


class CrawlerOutputConsumer(BufferedConsumer, PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                resource_name    VARCHAR(128) NOT NULL,
                source_name      VARCHAR(128) NOT NULL,
                data             TEXT
            )
        """

class CrawlerLogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def run_crawler(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:
        with CrawlerOutputConsumer(connection=conn, table_name=args.output, autocommit=True, truncate=True,
                                 buffer_size=10, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as output_consumer, \
                CrawlerLogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:
            Crawler = crawlers_manager.find_Crawler(args.resource_name, args.source_name)

            # output_consumer = FileConsumer('out/out.txt')
            # logs_consumer = FileConsumer(file_path='out/logs.txt')
            crawler = Crawler(output_consumer=output_consumer, logs_consumer=logs_consumer)
            crawler.crawl()
