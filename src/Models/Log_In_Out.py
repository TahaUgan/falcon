from Models.BaseModel import BaseModel
from Models.User import User
from Models.Loggers import e_logger, s_logger
from Models.Device import Device
from Models.Room import Room
import json
import falcon


class Login(BaseModel):

    def on_post(self, req, resp):

        on_login(User, req, resp)

class Logout(BaseModel):
 
    def on_post(self, req, resp):

        on_logout(User, req, resp)



    
def on_login(self, req, resp):
    raw_body = req.bounded_stream.read()
    data = json.loads(raw_body)
    username = data.get('username')
    password = data.get('password')
    room = data.get('room_ID')
    try:
        target_room = Room.select().where(Room.room_ID == room)
        target_room = target_room[0]
    except IndexError:
        resp.status = falcon.HTTP_404
        resp.body = json.dumps({"error": "Room not found"})
        e_logger.error("Attempted to login into non-existing room")
    if(not target_room):
        resp.status = falcon.HTTP_401
        resp.body = json.dumps({"error": "Room not found"})
        e_logger.error("Attempted to login into non-existing room")
    else:
        user = User.select().where(User.username == username, User.password == password)
        user = user[0]
        if(not user):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "Invalid Credentials"})
            s_logger.warning("Attempted to login with invalid credentials")
        else:
            if(user.session):
                resp.status = falcon.HTTP_401
                resp.body = json.dumps({"error": "You are already logged in a room"})
                e_logger.warning("Attempted to login while already logged in a room")
            else:
                device_id = user.device_ID
                device = Device.select().where(Device.device_ID == device_id)
                device = device[0]
                if(not device):
                    resp.status = falcon.HTTP_401
                    resp.body = json.dumps({"error": "User does not have an active device"})
                    e_logger.warning("attempted to login with no active device")
                elif(device.room_ID):
                    resp.status = falcon.HTTP_401
                    resp.body = json.dumps({"error": "You are already logged in a room"})
                    e_logger.warning("Attempted to login while already logged in a room")
                else:
                    user.session = "in " + str(room)
                    user.save()
                    device.room_ID = room
                    device.save()
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps({"message": "Logged in successfully"})
                    s_logger.info(f"user {user.username} logged in successfully, ID: {user.user_ID}")
def on_logout(self, req, resp):
    raw_body = req.bounded_stream.read()
    data = json.loads(raw_body)
    userID = data.get('ID')
    room = data.get('room_ID')
    target_room = Room.select().where(Room.room_ID == room)
    target_room = target_room[0]
    user = User.select().where(User.user_ID == userID)
    user = user[0]
    deviceID = user.device_ID
    user_device = Device.select().where(Device.device_ID == deviceID)
    user_device = user_device[0]
    if(not user.session):
        resp.status = falcon.HTTP_401
        resp.body = json.dumps({"error": "You are not logged in"})
        e_logger.error("Attempted to logout from non-existing room")
    else:
        if(not target_room.room_ID):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "The room you are trying to logout does not exist"})
            e_logger.error("Attempted to log out from non-existing room")
        else:
            room_session_text = "in " + str(target_room.room_ID)
            if(room_session_text != user.session):
                resp.status = falcon.HTTP_401
                resp.body = json.dumps({"error": "You are trying to log put from wrong room"})
                e_logger.error("Attempted to log out from a different room")
            else:
                user.session = None
                user_device.room_ID = None
                user.save()
                user_device.save()
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message": "Logged out successfully"})
                s_logger.info(f"user {user.username} logged out successfully, ID: {user.user_ID}")
