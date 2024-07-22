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

        ip = get_ip()

        headers = req.headers
        token = headers.get("TOKEN")
          
        from Models.Token import Token

        if not Token.check_token(token):
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            e_logger.error(f"Unauthorized access attempt with token: {token} - IP: {ip}")
            return

            
        

        headers_dict = req.headers
        auth = headers_dict.get("AUTHORIZATION")

        n = len(auth)

        auth = auth[6::]

        auth = base64.b64decode(auth)
        auth = auth.decode(encoding='utf-8')

        username = auth.split(":")[0]
        password = auth.split(":")[1]

        try:
            user = User.select().where(User.username == username, User.password == password).get()
        except DoesNotExist as e:
            resp.status = falcon.HTTP_203
            resp.body = "wrong username or password"
            
            e_logger.error(f"Failed log-in attempt from IP: {ip}")
            r_logger.error(f"Failed log-in request from IP: {ip}")
            return
        

        try:
            session = Sessions.get(Sessions.User_ID == user.user_ID, Sessions.End_Date == None)
            
            new_session_code = session.Session_Code
        except DoesNotExist as dne:
            new_session_code = generate_code(16)
            session = Sessions.create(Session_Code = str(new_session_code), user_ID = user.user_ID).save()
        
        user.session = new_session_code
        user.save()

        
         
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"Session_Code: ": new_session_code})

        s_logger.info(f"User with ID: {user.user_ID} has logged-in from IP: {ip}")



        

class Logout(BaseModel):

    def on_post(self, req, resp):

        ip = get_ip()

        headers_dict = req.headers
        
        token = headers_dict.get("TOKEN")

        from Models.Token import Token

        if not Token.check_token(token): #checking if token is invalid
            resp.status = falcon.HTTP_401
            resp.body = "You have no authority to do so"
            e_logger.error(f"Unauthorized access attempt with token: {token} - IP: {ip}")

            return

        given_code = headers_dict.get("SESSION-CODE")

        if not Sessions.check_session(given_code):
            resp.status = falcon.HTTP_401
            resp.body = "You don't have the authority to do so"
            r_logger.warning(f"No SESSION-CODE sent in the request headers. - IP: {ip}")
            return
    
        id = headers_dict.get("ID")
        

    
        if not id:
            resp.status = falcon.HTTP_400
            resp.body = "no id sent to log-out"
            r_logger.warning(f"No ID sent in the request headers. - IP: {ip}")


            
            return
       
    
        try:
            user = User.select().where(User.user_ID == id).get()
        except DoesNotExist as e:
            resp.status = falcon.HTTP_404
            resp.body = "there is no such user"
            e_logger.error(f"No user found with ID: {id} - IP: {ip}")

            return
        
            


        try:
            count = Sessions.select(fn.Count(Sessions.Session_Code)).where(Sessions.Session_Code == given_code)
        except:
            resp.status = falcon.HTTP_401
            resp.body = "Invalid session code"
            r_logger.warning(f"Invalid session code: {given_code} - IP: {ip}")

            return



        count = count.scalar()
        
    
            
        data = req.headers

        userID = data.get('ID')
        try:
            user = User.select().where(User.user_ID == userID, User.session != None).get()
        except DoesNotExist as e:
        
            resp.status = falcon.HTTP_400
            resp.body = "this user is not logged in"
            e_logger.warning(f"User with ID: {id} has tried to log out while not logged-in. - IP: {ip}")
            return


        session_code_to_remove = user.session
        user.session = None
        user.save()

        session = Sessions.select().where(Sessions.Session_Code == given_code).get()
        session.End_Date = fn.NOW()
        session.save()

        resp.status = falcon.HTTP_200
        resp.body = "Successfully logged-out"
        s_logger.info(f"User with ID: {id} successfully logged out - IP: {ip}")



        try:
            session_to_remove = Sessions.get(Sessions.Session_Code == session_code_to_remove)

            session_to_remove.delete_instance()
            
        except Exception as e:
            e_logger.warning(f"Error while deleting session: {session_code_to_remove} --> {e}")

    
        
    
    
def generate_code(N):

    session_code = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    return session_code


        





        



