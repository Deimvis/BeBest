import os
from bin.postgres import PostgresConnection, create_database



def run_init_db(args):
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=None,
            ) as conn:
        create_database(conn, args.db_name)
