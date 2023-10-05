import argparse
import logging
import os

import bin
import lib
from src.types.resources import ResourceName
from src.types.sources import SourceName


if os.getenv('DEBUG'):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt="%d/%b/%Y %H:%M:%S",
    )
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('yt').setLevel(logging.WARNING)
else:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
        datefmt="%d/%b/%Y %H:%M:%S",
    )


def parse_args():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--perf', type=str, help='Calculate perf and dump to specified path')
    parser = argparse.ArgumentParser(description='Datacamp binary')
    subparsers = parser.add_subparsers()
    subparsers.required = True

    init_db = subparsers.add_parser('init-db', parents=[common_parser])
    init_db.set_defaults(run=bin.run_init_db.run_init_db)
    init_db.add_argument('db_name', type=str)

    crawler = subparsers.add_parser('crawl', parents=[common_parser])
    crawler.set_defaults(run=bin.run_crawler.run_crawler)
    crawler.add_argument('resource_name', choices=ResourceName.all(), help='Resource name')
    crawler.add_argument('source_name', choices=SourceName.all(), help='Source name')
    crawler.add_argument('--output', type=str, help='Postgres table name', required=True)
    crawler.add_argument('--logs', type=str, help='Postgres table name', required=True)

    canonizer = subparsers.add_parser('canonize', parents=[common_parser])
    canonizer.set_defaults(run=bin.run_canonizer.run_canonizer)
    canonizer.add_argument('resource_name', choices=ResourceName.all(), help='Resource name')
    canonizer.add_argument('source_name', choices=SourceName.all(), help='Source name')
    canonizer.add_argument('--input', type=str, help='Postgres table name', required=True)
    canonizer.add_argument('--output', type=str, help='Postgres table name', required=True)
    canonizer.add_argument('--logs', type=str, help='Postgres table name', required=True)

    store = subparsers.add_parser('store', parents=[common_parser])
    store.set_defaults(run=bin.run_store.run_store)
    store.add_argument('resource_name', choices=ResourceName.all(), help='Resource name')
    store.add_argument('--input', type=str, help='Postgres table name', required=True)
    store.add_argument('--storage', type=str, help='Postgres table name', required=True)
    store.add_argument('--logs', type=str, help='Postgres table name', required=True)

    store = subparsers.add_parser('calc-features', parents=[common_parser])
    store.set_defaults(run=bin.run_calc_features.run_calc_features)
    store.add_argument('--user-logs', type=str, help='Postgres table name', required=True)
    store.add_argument('--storage', type=str, help='Postgres table name', required=True)
    store.add_argument('--logs', type=str, help='Postgres table name', required=True)

    store = subparsers.add_parser('rank', parents=[common_parser])
    store.set_defaults(run=bin.run_ranker.run_ranker)
    store.add_argument('--posts', type=str, help='Postgres table name', required=True)
    store.add_argument('--features', type=str, help='Postgres table name', required=True)
    store.add_argument('--logs', type=str, help='Postgres table name', required=True)

    store = subparsers.add_parser('calc-stats', parents=[common_parser])
    store.set_defaults(run=bin.run_calc_stats.run_calc_stats)
    store.add_argument('--vacancies', type=str, help='Postgres table name', required=True)
    store.add_argument('--storage', type=str, help='Postgres table name', required=True)
    store.add_argument('--logs', type=str, help='Postgres table name', required=True)

    return parser.parse_args()


def playground():
    from bin.postgres import PostgresConnection
    from lib.consumers import FileConsumer
    from src.types.resources import ResourceName
    from src.types.sources import SourceName
    from src.crawler import crawlers_manager

    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:
        with FileConsumer(file_path='out/out.txt') as output_consumer, \
                FileConsumer(file_path='out/logs.txt') as logs_consumer:
            Crawler = crawlers_manager.find_Crawler(ResourceName.POST, SourceName.HABR)

            crawler = Crawler(output_consumer=output_consumer, logs_consumer=logs_consumer)
            crawler.crawl()


    # with Consumer(file_path='out/test.txt', buffer_size=3, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as consumer:
    #     for i in range(7):
    #         consumer.recv({'hello': f'world! {i}'})


def main():
    args = parse_args()
    if args.perf is not None:
        args.run = lib.utils.perf.perf(args.perf)(args.run)
    args.run(args)


if __name__ == '__main__':
    main()
    # playground()
