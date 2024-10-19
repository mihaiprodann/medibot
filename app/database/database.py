import psycopg2
import logging
from psycopg2 import pool

def init_db(database_url):
    try:
        db_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10, database_url
        )
        if db_pool:
            logging.info("Database connection pool created successfully.")
            return db_pool
        else:
            logging.error("Database connection pool failed.")
            return None
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        return None

def execute_query(db_pool, query, params):
    conn = None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
    except Exception as e:
        logging.error(f"Failed to execute query: {e}")
    finally:
        if conn:
            db_pool.putconn(conn)

def create_tables(db_pool):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS meditatii (
            id SERIAL PRIMARY KEY,
            materie VARCHAR(255),
            data DATE,
            server_id VARCHAR(255)
        )
    '''
    execute_query(db_pool, create_table_query, ())
