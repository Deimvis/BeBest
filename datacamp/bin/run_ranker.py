import os
from tqdm import tqdm
from bin.postgres import PostgresConnection
from lib.consumers import BufferedConsumer, PostgresConsumer
from lib.storages.postgres.table import PostgresTable
from src.controller.posts.models import PostRecord
from src.ranker import PostRanker


class OutputConsumer(BufferedConsumer, PostgresConsumer):

    @property
    def create_table_query(self):
        return PostRecord.create_table_query()


class LogsConsumer(PostgresConsumer):

    @property
    def create_table_query(self):
        return """
            CREATE TABLE IF NOT EXISTS %s (
                insert_timestamp BIGINT,
                level            VARCHAR(32) NOT NULL,
                msg              TEXT NOT NULL
            )
        """


def run_ranker(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:

        posts = PostgresTable(conn, args.posts)
        features = PostgresTable(conn, args.features)
        new_posts = PostgresTable(conn, '_tmp_new_posts')
        with OutputConsumer(connection=conn, table_name=new_posts.table_name, autocommit=True, truncate=True,
                            buffer_size=10, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as output_consumer, \
                LogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:

            ranker = PostRanker()
            for row in tqdm(posts.select(), desc='Rank posts', total=posts.row_count(), position=0):
                post = PostRecord(**row)
                post_features_set = features.select(where={'post_canonized_url': post.canonized_url})
                match len(post_features_set):
                    case 0:
                        post_features = {}
                    case 1:
                        post_features = post_features_set[0]
                    case _:
                        raise RuntimeError(f'Invariant is broken, multiple features records found for post canonized url: {post.canonized_url}')
                rank = ranker.rank(post, post_features)
                new_post = post.model_copy(deep=True)
                new_post.rank = rank
                output_consumer.recv(new_post.model_dump())

        # new_posts.move(posts.table_name)
        with OutputConsumer(connection=conn, table_name=posts.table_name, autocommit=True, truncate=True,
                            buffer_size=100, overflow_mode=BufferedConsumer.OverflowMode.PARENT_CLASS) as output_consumer, \
                LogsConsumer(connection=conn, table_name=args.logs, autocommit=True, truncate=True) as logs_consumer:
            for row in tqdm(new_posts.select(), desc='Update post ranks', total=new_posts.row_count(), position=0):
                output_consumer.recv(row)
        new_posts.drop()
        posts.commit()
