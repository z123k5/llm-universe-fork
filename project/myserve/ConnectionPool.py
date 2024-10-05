import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.flushdb()

# Connect to the database
# 连接数据库
# 连接到 MongoDB
def connect_to_database():
    try:
        client = MongoClient('mongodb://{user}:{pwd}@{host}:{port}/{dbname}'.format(
                user=os.getenv('DB_USER_NAME'),
                pwd=os.getenv('DB_USER_PWD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                dbname=os.getenv('DB_NAME')
            ), 
            serverSelectionTimeoutMS=30000,    # Timeout for selecting a server
            socketTimeoutMS=45000,             # Timeout for operations on the socket
            retryWrites=True,                  # Enable retryable writes
            connect=True)                      # Enalbe auto_reconnect
        client.admin.command('ping')
        print('Success connect to ' + os.getenv('DB_NAME'))
        return client
    except ConnectionFailure as e:
        print('连接到 MongoDB 时出错:', e)
        return None

client = connect_to_database()
db = client.assistant_proj if client else None

assistants_collection = db.assistants
users_collection = db.users
