from Models.BaseModel import BaseModel
from peewee import *
from Utility.Loggers import e_logger, s_logger, r_logger
from Utility.GetIP import get_ip

import falcon
import json


class Room_logs(BaseModel):

    from Models.User import User
    from Models.Room import Room

    log_ID = IntegerField(primary_key=True)
    User_ID = ForeignKeyField(User, db_column='User_ID', backref='logs')
    Room_ID = ForeignKeyField(Room, db_column='Room_ID', backref='logs')
    Log_Type = CharField()
    Log_Date = DateField()


    def change_room(UserID, RoomID):

        from Models.Card import Card
        from Models.User import User
        from Models.Anchor import Anchor
        from Models.Room import Room
    
        card = (Card
                .select(Card)
                .join(User, on=Card.Card_ID == User.Card_ID)
                .where(User.user_ID == UserID)
                .get()
                )
        
        anchorID = Anchor.select(Anchor.Anchor_ID).join(Room, on=Anchor.Room_ID == Room.room_ID).where(Room.room_ID == RoomID)
       

        current_room = Anchor.select(Anchor.Room_ID).join(Card, on= Card.Anchor_ID == Anchor.Anchor_ID).where(Card.Card_ID == card.Card_ID)
        

        if not anchorID:
            return 0
        

        try:

            log = Room_logs.select().where(Room_logs.User_ID == UserID).order_by(Room_logs.log_ID.desc()).get()

        except DoesNotExist as dne:

            save = Room_logs.create(User_ID = UserID, Room_ID = RoomID, Log_Type = 'IN')
            save.save()

            card.Anchor_ID = anchorID
            card.save()
            
            return 1



        type = log.Log_Type

        if type == 'IN': #if last process was getting in to a room
            
            if current_room == RoomID: # if trying to get into the same room
                return 2
            else:
                save = Room_logs.create(User_ID = UserID, Room_ID = log.Room_ID, Log_Type = 'OUT') # first log user out of the room
                save.save

                
                save = Room_logs.create(User_ID = UserID, Room_ID = RoomID, Log_Type = 'IN') # then log user in the new room
                save.save()


                card.Anchor_ID = anchorID
                card.save()
                return 1

        else:
            save = Room_logs.create(User_ID = UserID, Room_ID = RoomID, Log_Type = 'IN')
            save.save()

            card.Anchor_ID = anchorID
            card.save()

            return 1

    def on_post_change_room(self, req, resp, userID):

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


        newRoomID = headers.get("ROOM-ID")
        # print(req.headers)

        # print(f"room id is : {newRoomID}")

        if not userID or not newRoomID:
            resp.status = falcon.HTTP_400
            resp.body = f"Missing Data"
            e_logger.error(f"Room change request with missing information, from IP: {get_ip()}")
            return



        res = Room_logs.change_room(userID, newRoomID)

        if res == 0:

            resp.status = falcon.HTTP_400
            resp.body = f"Missing or Invalid data"


        elif res == 1:
        
            resp.status = falcon.HTTP_200
            resp.body = f"succesfully moved"


        elif res == 2:

            resp.status = falcon.HTTP_400
            resp.body = f"You are already in this room"







    def on_get_past_users(self, req, resp, roomID):

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
        
        users = Room_logs.select(Room_logs.User_ID).distinct().where(Room_logs.Room_ID == roomID)

        resp.body = json.dumps([user for user in users.dicts()])