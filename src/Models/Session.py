from Models.User import User
from Models.Loggers import e_logger, s_logger, r_logger
from Models.BaseModel import BaseModel

from peewee import *


import random
import string

class Sessions(BaseModel):


    Session_Code = CharField(primary_key = True)
    Session_Start = DateField()
    Session_End = DateField()
    User_ID = ForeignKeyField(User, db_column = 'user_ID'  , backref = 'Sessions')





    