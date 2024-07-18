from peewee import *
from playhouse.pool import PooledMySQLDatabase
import falcon
import json
import logging



e_logger = logging.getLogger('errors')
e_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/error.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

e_logger.addHandler(ch)
e_logger.addHandler(fh)






s_logger = logging.getLogger('sessions')
s_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/session.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

s_logger.addHandler(ch)
s_logger.addHandler(fh)








# Define the database connection
db = PooledMySQLDatabase(
    'user',  # Replace with your database name
    user='root',  # Replace with your MariaDB username
    password='123456',  # Replace with your MariaDB password
    host='localhost',  # Replace with your MariaDB host
    port=3306  # Replace with your MariaDB port if different
)



# Define a model
class BaseModel(Model):
    class Meta:
        database = db




class Login(BaseModel):

    def on_post(self, req, resp):

        User.on_login(User, req, resp)

class Logout(BaseModel):

    def on_post(self, req, resp):

        User.on_logout(User, req, resp)

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





class Device(BaseModel):

    device_ID = IntegerField(primary_key=True)
    name = CharField()
    ID = ForeignKeyField(Room, db_column='room_ID', backref='devices')

    def on_get(self, req, resp):

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


        id = req.get_param('device_ID')

        if(not id):

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted creating device with no ID -> ID = " + str(id))


        else:

            name = req.get_param('name')
            roomid = req.get_param('room_ID')


            try:
                new_user = User.create(device_ID = id, name = name, room_ID = roomid)
                new_user.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("Device Created")
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "Device already exists"})
                e_logger.error("Attempted to create device with already existing ID -> ID = " + str(id))

    def on_delete(self, req, resp):

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


class User(BaseModel):

    user_ID = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField()
    password = CharField()
    session = CharField()
    device =ForeignKeyField(Device,db_column='device_ID', backref='users')

    def on_get(self, req, resp):



        # id = req.get_param('ID')
        user_list = []

        if(not id):
            user_list = User.select()
        else:
            user_list = list(User.select().dicts())
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

        user_list.append("made with 8001 port")

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