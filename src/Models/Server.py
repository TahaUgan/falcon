
from Models.BaseModel import BaseModel
from Models.Token import Token

from Models.Loggers import e_logger, s_logger, r_logger


from peewee import *

import falcon
import json



class Server(BaseModel):

    class Status():
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        UNKNOWN = 'unknown'

    server_ID = IntegerField(primary_key=True)
    server_Name = CharField()
    server_Status = CharField()