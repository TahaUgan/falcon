
from Models.BaseModel import BaseModel

from peewee import *


class Company(BaseModel):

    Company_ID = IntegerField(primary_key = True)
    Company_Name = CharField()
