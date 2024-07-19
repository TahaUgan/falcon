from Models.BaseModel import BaseModel
from peewee import *


class Token(BaseModel):

    token_Code = CharField(primary_key = True)
    access_Level = IntegerField()

    def get_access_level(token_code):

        access_level = Token.select(Token.access_Level).where(Token.token_Code == token_code)
        return access_level
    

