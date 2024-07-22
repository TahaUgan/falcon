from Models.BaseModel import BaseModel
from Models.User import User
from Models.Loggers import e_logger, s_logger, r_logger
from Models.Device import Device
from Models.Room import Room
from Models.GetIP import get_ip
from Models.Session import Sessions
from datetime import datetime
from peewee import *

import random
import string
import json
import falcon
import base64

class Login(BaseModel):

    def on_post(self, req, resp):

        headers = req.headers
        token = headers.get("TOKEN")
          
        from Models.Token import Token

        if not Token.check_token(token):
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return

            
        

        headers_dict = req.headers
        auth = headers_dict.get("AUTHORIZATION")

        n = len(auth)

        auth = auth[6::]

        auth = base64.b64decode(auth)
        auth = auth.decode(encoding='utf-8')

        print(f"auth vals are: {auth}")

        username = auth.split(":")[0]
        password = auth.split(":")[1]

        # username = data.get('username')
        # password = data.get('password')

        try:
            user = User.select().where(User.username == username, User.password == password).get()
        except DoesNotExist as e:
            resp.status = falcon.HTTP_203
            resp.body = "wrong username or password"
            IP = get_ip()

            e_logger.error("Failed log-in attempt from IP: " + str(IP))
            r_logger.error("Failed log-in request from IP: " + str(IP))
            return




    

        if not user.session:
            new_session_code = generate_code(16)
            user.session = new_session_code
            user.save()
            session = Sessions.create(Session_Code = str(new_session_code), user_ID = user.user_ID).save()

            message = "You have successfully logged-in"
            res = "Successfull"
        else:
            new_session_code = None
            message = "You already have a session"
            res = "Failed"
        return_dict = {}

        return_dict.update({"Message: ": message})
        return_dict.update({"Result: ": res})
        if new_session_code:
            return_dict.update({"Session: ": new_session_code})
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(return_dict)



        

class Logout(BaseModel):

    def on_post(self, req, resp):

        headers_dict = req.headers
        
        token = headers_dict.get("TOKEN")

        from Models.Token import Token

        if not Token.check_token(token):
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            return

    
        id = headers_dict.get("ID")
        
        print(f"id bool is this: {not id}")

    
        if not id:
            resp.status = falcon.HTTP_204
            resp.body = "No ID sent"
            print("Yeah, no id sent here")
            return
        else:
            print(f"id is: {id}")
    
        try:
            user = User.select().where(User.user_ID == id).get()
        except DoesNotExist as e:
            resp.status = falcon.HTTP_404
            resp.body = "there is no such user"
            return
        
            
        given_code = headers_dict.get("SESSION-CODE")
        try:
            count = Sessions.select(fn.Count(Sessions.Session_Code)).where(Sessions.Session_Code == given_code)
        except:
            pass
            # TO-DO fill here


        count = count.scalar()
        
    
        if (not count) or (not given_code):
            resp.status = falcon.HTTP_401
            resp.body = "Request Invalid"
    
        else:
            
            data = req.headers
    
            userID = data.get('ID')
            try:
                user = User.select().where(User.user_ID == userID, User.session != None).get()
            except DoesNotExist as e:
            
                resp.status = falcon.HTTP_400
                resp.body = "this user is not logged in"
                return
    
    
    
            user.session = None
            user.save()
    
            session = Sessions.select().where(Sessions.Session_Code == given_code).get()
            session.End_Date = fn.NOW()
            session.save()
    
            resp.status = falcon.HTTP_200
            resp.body = "Successfully logged-out"
    
    
    
        
    
    
def generate_code(N):

    session_code = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    return session_code


        





        



