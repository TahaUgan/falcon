
from Models.BaseModel import BaseModel
from Models.Room import Room
from Models.Token import Token
from Models.Session import Sessions
from Models.Loggers import e_logger, s_logger, r_logger

from peewee import *

import falcon
import json


class Anchor(BaseModel):

    Anchor_ID = IntegerField(primary_key=True)
    Anchor_Name = CharField()
    Room_ID = ForeignKeyField(Room, db_column = 'Room_ID', backref = 'anchors')
    Anchor_Status = CharField()


    def on_get(self, req, resp):

               
        headers = req.headers
        
        id = headers.get("ID")
        name = headers.get("NAME")
        roomID = headers.get("ROOM_ID")
        status = headers.get("STATUS")

        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return
        
        filters = []
        
        if id:
            filters.append(Anchor.Anchor_ID == id)
        if name:
            filters.append(Anchor.Anchor_Name == name)
        if roomID:
            filters.append(Anchor.Room_ID == roomID)
        if status:
            filters.append(Anchor.Anchor_Status == status)


        if filters:
            anchors = Anchor.select().where(*filters)
        else:
            anchors = Anchor.select()

        # Convert to dictionaries and create the response
        anchors = [anchor for anchor in anchors.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(anchors)






        



