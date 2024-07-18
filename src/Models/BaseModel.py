from peewee import *
from playhouse.pool import PooledMySQLDatabase




db = PooledMySQLDatabase(
    'user',  # Replace with your database name
    user='root',  # Replace with your MariaDB username
    password='123456',  # Replace with your MariaDB password
    host='localhost',  # Replace with your MariaDB host
    port=3306  # Replace with your MariaDB port if different
)


class BaseModel(Model):
    class Meta:
        database = db

