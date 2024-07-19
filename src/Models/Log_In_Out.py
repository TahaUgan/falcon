from Models.BaseModel import BaseModel
from Models.User import User
from Models.Loggers import e_logger, s_logger, r_logger
from Models.Device import Device
from Models.Room import Room
from Models.GetIP import get_ip
from Models.Session import Sessions
from datetime import datetime
from peewee import *

import json
import falcon


class Login(BaseModel):

    def on_post(self, req, resp):

        login(User, req, resp)

class Logout(BaseModel):

    def on_post(self, req, resp):

        logout(User, req, resp)



    
def login(self, req, resp):


    raw_body = req.bounded_stream.read()
    data = json.loads(raw_body)


    username = data.get('username')
    password = data.get('password')
    
    user = User.select().where(User.username == username, User.password == password)[0]

    IP = get_ip()
    if(not user):
        resp.status = falcon.HTTP_203
        resp.body = json.dumps("Wrong username/password")


        e_logger.error("Failed log-in attempt from IP: " + str(IP))
        r_logger.error("Failed log-in request from IP: " + str(IP))
    else:

        print(f"session is: {user.session}")
        if(not user.session):


            res = user.assign_session()
            print(res)

            if(res):

                current = datetime.now()
                session = session.create(session_code = user.session, session_start = current, user_ID = user.user_ID)

                r_logger.info(f"User with user_ID: {user.user_ID} has been assigned a new session from IP: {IP}")

                resp.status = falcon.HTTP_200
                resp.body = json.dumps("Successfully logged in")
            else:
                resp.body = "Something went wring"
       

        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps("This user already has a session")
            e_logger.warning(f"Attempted to get a new session whioe having session, user ID: {user.user_ID} and IP: {IP}")

        



def logout(self, req, resp):

    raw_body = req.bounded_stream.read()
    data = json.loads(raw_body)
    userID = data.get('ID')

    user_count = User.select(fn.count(User.user_ID)).where(User.user_ID == userID)
    
    IP = get_ip()

    if(user_count):
        
        user = User.select().where(User.user_ID == userID)[0]

        if(not user.session):
        
            resp.status = falcon.HTTP_400
            resp.body = json.dumps("You don't have a session to log-out from")

            e_logger.error(f"Attempted to log out while not having a session, user ID: {user.user_ID} and IP: {IP}")
            r_logger.info(f"Attemp to log out while not logged-in, user ID: {user.user_ID} and IP: {IP}")
        
        else:

            user.session = None
            user.save()

            resp.status = falcon.HTTP_200
            resp.body = f"Successfully log-out"

            s_logger.info(f"User with user ID: {user.user_ID} has logged out, IP: {IP}")




    




