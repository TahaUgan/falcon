from Models.BaseModel import BaseModel
from Utility.Loggers import e_logger, s_logger

from Utility.GetIP import get_ip
from Models.Place import Place

from peewee import *
import falcon
import json




class Room(BaseModel):

    room_ID = IntegerField(primary_key=True)
    room_Name = CharField()
    Place_ID = ForeignKeyField(Place, db_column = 'Place_ID', backref='rooms')

    def on_get(self, req, resp):
        
        headers = req.headers

        id = headers.get("ID")
        name = headers.get("NAME")
        placeID = headers.get("PLACE_ID")
        session = headers.get("SESSION")
        token = headers.get("TOKEN")


        from Models.Session import Sessions
        from Utility.Token import Token

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        from Models.Session import Sessions
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return

        filters = []

        if id:
            filters.append(Room.room_ID == id)
        if name:
            filters.append(Room.room_Name == name)
        if placeID:
            filters.append(Room.Place_ID == placeID)

        if filters:
            rooms = Room.select().where(*filters)
        else:
            rooms = Room.select()


        rooms = [room for room in rooms.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(rooms)


        





    
    def on_get_users_count(self, req, resp):

        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return



        from Models.Anchor import Anchor
        from Models.Card import Card
        from Models.User import User

        users_count = (Room
                       .select(Room.room_ID, fn.Count(User.user_ID))
                       .join(Anchor, on=Room.room_ID == Anchor.Room_ID)
                       .join(Card, on=Anchor.Anchor_ID == Card.Anchor_ID)
                       .join(User, Card.Card_ID == User.Card_ID)
                       .where(User.Card_ID != None)
                       .group_by(Room.room_ID) 
                       )


        users_count = [count for count in users_count.dicts()]


        resp.status = falcon.HTTP_200
        resp.body = json.dumps(users_count)


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



    def on_get_cards_rooms(self ,req, resp):


        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        from Utility.Token import Token
        from Models.Session import Sessions

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        
        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return
        
        from Models.Card import Card
        from Models.Anchor import Anchor

        cards = (Card
                 .select(Room.room_ID, Card.Card_ID)
                 .join(Anchor, on=Card.Anchor_ID == Anchor.Anchor_ID)
                 .join(Room, on= Room.room_ID == Anchor.Room_ID)
                 
                 )
        
        cards = [card for card in cards.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(cards)
