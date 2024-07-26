from peewee import *
from Models.BaseModel import BaseModel
from Models.Room import Room
from Utility.GetIP import get_ip
from Utility.Loggers import e_logger, s_logger

import falcon
import json



class Device(BaseModel):

    device_ID = IntegerField(primary_key=True)
    name = CharField()
    ID = ForeignKeyField(Room, db_column='room_ID', backref='devices')

    def on_get(self, req, resp):

         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Utility.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    

        id = req.get_param('device_ID')
        device_list = []

        filters = []

        if(not id):
            devices = Device.select()
        else:
            filters.append(Device.ID == id)

            name = req.get_param('name')
            room_id = req.get_param('room_ID')

            if(name):
                filters.append(Device.name == name)
            if(room_id):
                filters.append(Device.room_ID == room_id)

            devices = Device.select().where(filters)


        for device in devices:
            device_data = device.__data__
            device_tuple = tuple(device_data.values())
            device_list.append(device_tuple)


        if(len(device_list) == 0):
            resp.status = falcon.HTTP_204
            resp.body = json.dumps("device Not Found")
        else:

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(device_list)









    def on_post(self, req, resp):

         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Utility.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    


        id = req.get_param('device_ID')

        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted creating device with no ID -> ID = " + str(id))


        else:

            name = req.get_param('name')
            roomid = req.get_param('room_ID')


            try:
                from Models.User import User
                new_user = User.create(device_ID = id, name = name, room_ID = roomid)
                new_user.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("Device Created")
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "Device already exists"})
                e_logger.error("Attempted to create device with already existing ID -> ID = " + str(id))

    def on_delete(self, req, resp):

         
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions
        from Utility.Token import Token

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return
    

        id = req.get_param('device_ID')

        filters = []

        if (not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted deleting device with no ID -> ID = " + str(id))

        else:

            filters.append(Room.ID == id)

            name = req.get_param('name')

            if (name):
                filters.append(Device.name == name)

            try:
                Device.delete().where(filters).execute()

                resp.status = falcon.HTTP_200
            except IntegrityError:
                resp.status = falcon.HTTP_204
                resp.body = json.dumps({"error": "Device Not Found"})
                e_logger.error("Attempted delete non-existing device")

