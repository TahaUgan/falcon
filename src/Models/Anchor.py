
from Models.BaseModel import BaseModel
from Models.Room import Room

from Utility.Loggers import e_logger, s_logger, r_logger
from Utility.GetIP import get_ip

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
        

        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

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
      
      
        id = headers.get("ID")
        name = headers.get("NAME")
        roomID = headers.get("ROOM_ID")
        status = headers.get("STATUS")
        
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


    def on_get_matching_cards(self, req, resp):

        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

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


        from Models.Card import Card

        anchor_card = (Anchor
                       .select(Anchor.Anchor_ID, Card.Card_ID)
                       .join(Card, on=(Anchor.Anchor_ID == Card.Anchor_ID))
                       
                    )
        

        anchor_card = [ancard for ancard in anchor_card.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(anchor_card)















    def on_delete(self, req, resp):

                 
        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

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

        id = headers.get("ID")
        name = headers.get("NAME")
        roomID = headers.get("ROOM_ID")
        status = headers.get("STATUS")
        

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
            Anchor.delete().where(*filters)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps("Anchors have been removed")
            r_logger.info(f"anchors has been removed with filter: {filters[0]}, IP: {get_ip()}")
        else:
            resp.status = falcon.HTTP_400
            resp.body = "No anchor found with these/this filters"
            e_logger.info(f"Failed anchor remove attempt, no anchor found, IP: {get_ip()}")


    def on_post(self, req, resp):
        
        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

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


        id = headers.get("ID")
        name = headers.get("NAME")
        roomID = headers.get("ROOM_ID")
        status = headers.get("STATUS")

        if not id:
            resp.status = falcon.HTTP_206
            resp.body = "Anchor must have an ID"
            e_logger.error(f"Attempted creating anchor with no ID, IP: {get_ip()}")
        
        filters = []
        
        if id:
            filters.append(Anchor_ID = id)
        if name:
            filters.append(Anchor_Name = name)
        if roomID:
            filters.append(Room_ID = roomID)
        if status:
            filters.append(Anchor_Status = status)

        anchor = Anchor.create(*filters)

        anchor.save()




