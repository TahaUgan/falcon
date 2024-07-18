from peewee import *
from playhouse.pool import PooledMySQLDatabase

import configparser

config = configparser.ConfigParser()
config.read("authorization.ini")
dbinfo = config["mariadb"]

dbname = dbinfo["database"]
dbuser = dbinfo["username"]
dbpassword = dbinfo["password"]
dbhost = dbinfo["hostname"]
dbport = dbinfo["port"]

dbport = int(dbport)


db = PooledMySQLDatabase(
    dbname,  # Replace with your database name
    user = dbuser,  # Replace with your MariaDB username
    password = dbpassword,  # Replace with your MariaDB password
    host = dbhost,  # Replace with your MariaDB host
    port = dbport  # Replace with your MariaDB port if different
)


class BaseModel(Model):
    class Meta:
        database = db

