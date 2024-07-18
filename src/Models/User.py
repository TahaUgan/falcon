from peewee import *
from Models.BaseModel import BaseModel, db
from Models.Loggers import e_logger, s_logger
from Models.Device import Device
import falcon
import json





class User(BaseModel):

    user_ID = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField()
    password = CharField()
    session = CharField()
    device =ForeignKeyField(Device,db_column='device_ID', backref='users')

    def on_get(self, req, resp):



        id = req.get_param('ID')
        user_list = []

        if(not id):
            user_list = User.select()
        else:
            user_list = list(User.select().where(User.user_ID == id).dicts())
            # print(user_list)
            # print(User.ID)
        #
        # for user in users:
        #     user_data = user.__data__
        #     user_tuple = tuple(user_data.values())
        #     user_list.append(user_tuple)


        if(len(user_list) == 0):

            user_list = "No Users Found"
            resp.status = falcon.HTTP_204

        else:
            resp.status = falcon.HTTP_200

        # user_list.append("made with 8001 port")
        user_list.capitalize()

        resp.body = json.dumps(user_list)







    def on_post(self, req, resp):

        cursor = db.cursor()

        id = req.get_param('ID')
        

        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted creating user with no ID -> ID = " + str(id))


        else:

            username = req.get_param('username')
            password = req.get_param('password')
            email = req.get_param('email')
            session = req.get_param('session')
            device_ID = req.get_param('device_ID')


            try:
                new_user = User.create(ID = id, username = username, email = email, password = password, session = session, device_ID = device_ID)
                new_user.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("User Created")
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "User already exists"})
                e_logger.error("Attempted to create user with already existing ID -> ID = " + str(id))


    def on_delete(self, req, resp):

        id = req.get_param('ID')
        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted deleting user with no ID -> ID = " + str(id))

        else:
            username = req.get_param('username')
            password = req.get_param('password')
            email = req.get_param('email')
            session = req.get_param('session')
            device_ID = req.get_param('device_ID')


            filter = []

            filter.append(User.ID == id)



            if(username):
                filter.append(User.username == username)
            if(password):
                filter.append(User.password == password)
            if(email):
                filter.append(User.email == email)
            if(device_ID):
                filter.append(Device.device_ID == device_ID)
            if(session):
                filter.append(User.session == session)


            try:
                User.delete().where(filter).execute()

                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message": "User Deleted"})
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "User does not exist"})
                e_logger.error("Attempted to delete non-existing user")

