import random
import string
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
    
    user = User.select().where(User.username == username, User.password == password).get()

    IP = get_ip()
    if(not user):
        resp.status = falcon.HTTP_203
        resp.body = json.dumps("Wrong username/password")


        e_logger.error("Failed log-in attempt from IP: " + str(IP))
        r_logger.error("Failed log-in request from IP: " + str(IP))
    else:

        new_session_code = generate_code(16)
        

        user.session = new_session_code
        user.save()

        session = Sessions.create(Session_Code = str(new_session_code), user_ID = user.user_ID).save()
        

        resp.status = falcon.HTTP_200
        resp.body = new_session_code

        



def logout(self, req, resp):

    headers_dict = req.headers

    given_code = headers_dict.get("SESSION-CODE")
    

    count = Sessions.select(fn.Count(Sessions.Session_Code)).where(Sessions.Session_Code == given_code)
    count = count.scalar()
    

    if (not count) or (not given_code):
        resp.status = falcon.HTTP_401
        resp.body = "Request Invalid"

    else:
        raw_body = req.bounded_stream.read()
        data = json.loads(raw_body)
        userID = data.get('ID')
        user = User.select().where(User.user_ID == userID).get()
        user.session = None
        user.save()

        session = Sessions.select().where(Sessions.Session_Code == given_code).get()
        session.



    


def generate_code(N):

    session_code = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    return session_code
