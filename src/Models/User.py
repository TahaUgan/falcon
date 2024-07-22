from peewee import *
from Models.BaseModel import BaseModel, db
from Models.Loggers import e_logger, s_logger, r_logger
from Models.Device import Device
from Models.GetIP import get_ip
from Models.Token import Token

import random
import string
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

        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        IP = get_ip()
        from Models.Session import Sessions

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            s_logger.warning(f"Unauthorized GET request from IP: {IP}")
            r_logger.warning(f"Unauthorized GET request from IP: {IP}")
            return


        id = req.get_param('ID')
        user_list = []

        if(not id):
            user_list = User.select()
        else:
            user_list = User.select().where(User.user_ID == id)
  

        user_list = list(user_list.dicts())
     

        if(len(user_list) == 0):

            user_list = "No Users Found"
            resp.status = falcon.HTTP_204

        else:
            resp.status = falcon.HTTP_200

        resp.body = json.dumps(user_list)

        r_logger.info(f"Device with IP: {IP} has accessed users")





    def on_post(self, req, resp):

        IP = get_ip()
        
        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            s_logger.warning(f"Unauthorized GET request from IP: {IP}")
            r_logger.warning(f"Unauthorized GET request from IP: {IP}")
            return

        id = req.get_param('ID')
        
        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error(f"Attempted creating user with no ID -> ID = {id}")

        else:

            username = req.get_param('username')
            password = req.get_param('password')
            email = req.get_param('email')
            session = req.get_param('session')
            device_ID = req.get_param('device_ID')

            try:
                new_user = User.create(user_ID = id, username = username, email = email, password = password, session = session, device_ID = device_ID)
                new_user.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("User Created")
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "User already exists"})
                e_logger.error(f"Attempted to create user with already existing ID -> ID: {id}, IP: {IP}")
                r_logger.error(f"Attempted to create user with already existing ID -> ID: {id}, IP: {IP}")


    def on_delete(self, req, resp):

        IP = get_ip()

        headers = req.headers

        session = headers.get("SESSION")
        token = headers.get("TOKEN")

        from Models.Session import Sessions

        is_session = Sessions.check_session(session)
        is_token = Token.check_token(token)

        if not is_session or not is_token:
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            s_logger.warning(f"Unauthorized GET request from IP: {IP}")
            r_logger.warning(f"Unauthorized GET request from IP: {IP}")
            return

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

            filter.append(User.user_ID == id)



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
                r_logger.error("Attempted to delete non-existing user")





    def assign_session(self):

        

        session_code = User.generate_code(16)
        
        IP = get_ip()

        count = User.select(fn.count(User.user_ID)).where(User.session == session_code).get()


        if(count != 0): # means that there is no userwith that session code
            self.session = session_code
            self.save()
            
            s_logger.info(f"New session has been assigned to user_ID: {self.user_ID} with IP: {IP}")
            
        else:
            if(self.user_ID != self.user_ID):
                User.assign_session(self)
            else:
                e_logger.warning(f"User with ID: {self.user_ID} has tried to login while having session from IP: {IP}")
                r_logger.info(f"Request to login with existing user, user ID: {self.user_ID} from IP: {IP}")

        return session_code


    

    def generate_code(N):

        session_code = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
        return session_code

