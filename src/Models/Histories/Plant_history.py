from Models.BaseModel import BaseModel
from peewee import *


class Plant_history(BaseModel):

    History_ID = IntegerField(primary_key=True)
    Plant_ID = IntegerField()
    Plant_Name = CharField()
    Company_ID = IntegerField()
    Server_ID = IntegerField()
    Change_Date = DateField()
    Is_Last = CharField()


