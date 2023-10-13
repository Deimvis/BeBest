import os
from pathlib import Path
from bin.postgres import PostgresConnection
from lib.consumers import BufferedConsumer, PostgresConsumer
from src.scrapers import scrapers_manager


class ScraperOutputConsumer(BufferedConsumer, PostgresConsumer):

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

class ScraperLogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def run_scraper(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:
        with ScraperOutputConsumer(connection=conn, table_name=args.output, autocommit=True, truncate=True,
                                 buffer_size=10, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as output_consumer, \
                ScraperLogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:
            Scraper = scrapers_manager.find_Scraper(args.resource_name, args.source_name)

            # from lib.consumers import FileConsumer
            # output_consumer = FileConsumer(file_path='out/out.txt')
            # logs_consumer = FileConsumer(file_path='out/logs.txt')

            if args.plan_file_path:
                plan_file = Path(args.plan_file_path)
            else:
                plan_file = Path(os.getenv('FILES_DIR_PATH')) / 'plans' / f'{args.resource_name}_{args.source_name}.json'
            plan = Scraper.plan_type().model_validate_json(plan_file.read_text())
            scraper = Scraper(output_consumer=output_consumer, logs_consumer=logs_consumer)
            scraper.scrape(plan)
