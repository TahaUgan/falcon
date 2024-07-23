from Models.User import User
from Models.Loggers import e_logger, s_logger, r_logger
from Models.BaseModel import BaseModel

from peewee import *

import random
import string

class Sessions(BaseModel):


    Session_Code = CharField(primary_key = True)
    End_Date = DateTimeField()
    User_ID = ForeignKeyField(User, db_column = 'user_ID'  , backref = 'Sessions')


    def check_session(token):

        try:
            from Models.Session import Sessions
            count = Sessions.select(fn.Count(Sessions.Session_Code)).where(Sessions.Session_Code == token)
        except:
            pass
            
            # TO-DO fill here
        count = count.scalar()

        return count>=1






    