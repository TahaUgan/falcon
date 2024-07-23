
from Models.BaseModel import BaseModel
from Models.Token import Token
from Models.Session import Sessions

from peewee import *

import falcon
import json

class Company(BaseModel):

    Company_ID = IntegerField(primary_key = True)
    Company_Name = CharField()


    def on_get(self, req, resp):


        headers = req.headers

        id = headers.get("ID")
        name = headers.get("NAME")

        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        if not token:
            resp.status = falcon.HTTP_400
            resp.body = "Missing authenticative data"

            #to-do update log files
            return

        if not session:
            resp.status = falcon.HTTP_400
            resp.body = "Missing authenticative data"

            #to-do update log files
            return
        
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = "You don't have the authority to do so"

            #to-do update log files
            return

    
        filters = []
        filters.append(True)


        if id:
            filters.append(Company.Company_ID == id)
        
        if name:
            filters.append(Company.Company_Name == name)

        print("HERE1")
        return

        companies = Company.select(filters).dicts()


        resp.status = falcon.HTTP_200
        resp.body = companies















