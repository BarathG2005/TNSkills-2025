import mysql.connector
from mysql.connector import pooling
from functools import lru_cache

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123",
    "database": "tnskills"
}
@lrc_cache
def get_pool():
    return  pooling.MySQLConnectionPool(
    pool_name="feetmanag",
    pool_size=5,
    **db_config
    )

def get_db():
    return get_pool().get_connection()