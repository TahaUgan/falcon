from peewee import *
from Models.BaseModel import BaseModel
from Models.Anchor import Anchor
from Utility.GetIP import get_ip
from Utility.Loggers import e_logger, s_logger

import falcon
import json



class Card(BaseModel):

    Card_ID = IntegerField(primary_key=True)
    Card_Name = CharField()
    Anchor_ID = ForeignKeyField(Anchor, db_column='Anchor_ID', backref='cards')

    def on_get(self, req, resp):

         
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
    

        id = req.get_param('Card_ID')

        filters = []

        if(not id):
            cards = Card.select()
        else:
            filters.append(Card.ID == id)

            name = req.get_param('name')
            room_id = req.get_param('room_ID')

            if(name):
                filters.append(Card.name == name)
            if(room_id):
                filters.append(Card.room_ID == room_id)

            cards = Card.select().where(filters)

            cards = [card for card in cards]


        if not cards:
            resp.status = falcon.HTTP_204
            resp.body = json.dumps("Card Not Found")
        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(cards)









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
    


        id = req.get_param('Card_ID')

        if not id:

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted creating Card with no ID -> ID = " + str(id))


        else:

            name = req.get_param('Card_Name')
            anchorID = req.get_param('anchor_ID')


            try:
                from Models.User import User
                new_user = User.create(Card_ID = id, Card_Name = name, Anchor_ID = anchorID)
                new_user.save()

                resp.status = falcon.HTTP_201
                resp.body = json.dumps("Card Created")
            except IntegrityError:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({"error": "Card already exists"})
                e_logger.error("Attempted to create card with already existing ID -> ID = " + str(id))

    def on_delete(self, req, resp):

         
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
    

        id = req.get_param('Card_ID')

        filters = []

        if not id:

            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "ID field required"})
            e_logger.error("Attempted deleting card with no ID -> ID = " + str(id))

        else:

            filters.append(Card.Card_ID == id)

            name = req.get_param('Card_Name')

            if name:
                filters.append(Card.Card_Name == name)

            try:
                Card.delete().where(filters).execute()

                resp.status = falcon.HTTP_200
            except IntegrityError:
                resp.status = falcon.HTTP_204
                resp.body = json.dumps({"error": "Card Not Found"})
                e_logger.error("Attempted delete non-existing card")

