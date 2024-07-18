from peewee import *
from Models.BaseModel import BaseModel
from Models.Loggers import e_logger, s_logger


import falcon
import json




class Room(BaseModel):

    room_ID = IntegerField(primary_key=True)
    name = CharField()

    def on_get(self, req, resp):

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


        for room in rooms:
            room_data = room.__data__
            room_tuple = tuple(room_data.values())
            room_list.append(room_tuple)


        if(len(room_list) == 0):
            resp.status = falcon.HTTP_204
            resp.body = json.dumps("Room Not Found")
        else:

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(room_list)


    def on_get(self, req, resp, room_ID):
        
        from Models.Device import Device
        from Models.User import User

        


        # users = []

        # for devID in device_IDs:
        #     user = User.select().where(User.device_ID == devID)[0]
        #     users.append(user)


        # resp.status = falcon.HTTP_200
        # resp.body = json.dumps(users)

        subquery = (Device
            .select(Device.device_ID.alias('devID'))
            .join(Room, on=(Device.room_ID == Room.room_ID))
            .alias('A'))

        # Main query
        query = (User
            .select(User.user_ID)
            .join(subquery, on=(User.device_ID == subquery.c.devID)))

        # Execute the query
        result = query.execute()

        # result = list(result.dicts())

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)




    def on_post(self, req, resp):

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








