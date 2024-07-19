from Models.User import User
from Models.Loggers import e_logger, s_logger, r_logger
from Models.BaseModel import BaseModel

from peewee import *


import random
import string

class Sessions(BaseModel):


    session_code = CharField(primary_key = True)
    session_start = DateField()
    session_end = DateField()
    user_ID = ForeignKeyField(User, db_column = 'user_ID'  , backref = 'sessions')





    