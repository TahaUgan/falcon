
from Models.BaseModel import BaseModel
from Utility.Token import Token
from Utility.Loggers import e_logger, s_logger, r_logger
from Utility.GetIP import get_ip
from Models.Plant import Plant

from peewee import *

import falcon
import json


class Place(BaseModel):

    Place_ID = IntegerField(primary_key=True)
    Place_Name = CharField()
    Plant_ID = ForeignKeyField(Plant, db_column = 'Plant_ID',backref='places')


    def on_get(self, req, resp):
        headers = req.headers

        id = headers.get("ID")
        name = headers.get("NAME")
        plant_id = headers.get("PLANT_ID")

        token = headers.get("TOKEN")
        session = headers.get("SESSION")

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
        
        filters = []
        if id:
            filters.append(Place.Place == id)
        if name:
            filters.append(Place.Place == name)
        if plant_id:
            filters.append(Place.Plant_ID == plant_id)

        try:
            if filters:
                query = Place.select().where(*filters)
            else:
                query = Place.select()
            
            places = [place for place in query.dicts()]
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(places)
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({"error": "Internal Server Error"})
            e_logger.error(f"GET /Places => {str(e)}")




    def on_get_rooms(self, req, resp, placeID):
        
        
        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        from Models.Session import Sessions
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return
        

        from Models.Room import Room

        rooms = Room.select().where(Room.Place_ID == placeID)
        
        rooms = [room for room in rooms.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(rooms)



        

    def on_delete(delf, req, resp):

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
        plant_id = headers.get("PLANT_ID")



        filters = []
        if id:
            filters.append(Place.Place == id)
        if name:
            filters.append(Place.Place == name)
        if plant_id:
            filters.append(Place.Plant_ID == plant_id)



        if filters:
            Place.delete().where(*filters)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps("Places have been removed")
            r_logger.info(f"Places has been removed with filter: {filters[0]}, IP: {get_ip()}")
        else:
            resp.status = falcon.HTTP_400
            resp.body = "No place found with these/this filters"
            e_logger.info(f"Failed place remove attempt, no place found, IP: {get_ip()}")




