from peewee import *
from Models.BaseModel import BaseModel
from Models.Loggers import e_logger, s_logger
from Models.GetIP import get_ip

import falcon
import json




class Room(BaseModel):

    room_ID = IntegerField(primary_key=True)
    name = CharField()

    def on_get(self, req, resp):

        
        
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Models.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    

        id = req.get_param('ID')
        room_list = []


        filters = []

        if(not id):
            rooms = Room.select()
        else:
            filters.append(Room.room_ID == id)

            name = req.get_param('name')

            if(name):
                filters.append(Room.name == name)

            rooms = Room.select().where(filters)

        rooms = list(rooms.dicts())

        resp.body = json.dumps(rooms)


    
    def on_get_users(self, req, resp, room_ID):
        
        from Models.Device import Device
        from Models.User import User

         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Models.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    
        

        
        query = (User
         .select(User)
         .join(Device, on=(User.device_ID == Device.device_ID))
         .join(Room, on=(Device.room_ID == Room.room_ID))
         .where(Room.room_ID == room_ID))


        

        result = list(query.dicts())

        

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)





    def on_post(self, req, resp):

         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Models.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    

        id = req.get_param('ID')

        if(not id):
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted creating room with no ID -> ID = " + str(id))
        else:

            name = req.get_param('name')

            try:

                new_room = Room.create(ID = id, Name = name)
                new_room.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("Room Created")

            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "Room already exists"})
                e_logger.error("Attempted creating room with already existing ID -> ID = " + str(id))





    def on_delete(self, req, resp):
         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Models.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    
        
        id = req.get_param('ID')

        filters = []

        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted deleting room with no ID -> ID = " + str(id))

        else:

            filters.append(Room.ID == id)

            name = req.get_param('name')

            if(name):
                filters.append(Room.name == name)

            try:
                Room.delete().where(filters).execute()

                resp.status = falcon.HTTP_200

            except IntegrityError:

                resp.status = falcon.HTTP_204
                resp.body = json.dumps({"error": "Room Not Found"})
                e_logger.error("Attempted delete non-existing room")








