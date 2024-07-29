
from Models.BaseModel import BaseModel
from Utility.GetIP import get_ip
from Utility.Loggers import e_logger, s_logger, r_logger


from peewee import *

import falcon
import json



class Server(BaseModel):

    class Status():
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        UNKNOWN = 'unknown'

    server_ID = IntegerField(primary_key=True)
    server_Name = CharField()
    server_Status = CharField()



    def on_get(self, req, resp):

                 
        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        id = headers.get("ID")
        name = headers.get("NAME")
        status = headers.get("STATUS")


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
        


        filters = []

        if id:
            filters.append(Server.Server_ID == id)
        if name:
            filters.append(Server.Server_Name == name)
        if status:
            filters.append(Server.Server_Status == status)

        if filters:
            servers = Server.select().where(*filters)
        else:
            servers = Server.select()


        servers = [server for server in servers.dicts()]


        if servers:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(servers)
            r_logger.info(f"Card with IP: {get_ip()} has accessed servers")

        else:
            resp.status = falcon.HTTP_400
            resp.body = "No data found"
            r_logger.info(f"Card with IP: {get_ip()} couldn't find any server")



    def on_get_anchors(self, req, resp, serverID):

        from Models.Anchor import Anchor
        from Models.Room import Room
        from Models.Place import Place
        from Models.Plant import Plant
        from Models.Server import Server
                 
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


        anchors = (Anchor
                   .select(Anchor)
                   .join(Room, on=(Anchor.Room_ID == Room.room_ID))
                   .join(Place, on=(Room.Place_ID == Place.Place_ID))
                   .join(Plant, on=(Place.Plant_ID == Plant.plant_ID))
                   .join(Server, on=(Plant.server_ID == Server.server_ID))
                   .where(Server.server_ID == serverID)
                   )
        

        anchors = [anchor for anchor in anchors.dicts()]

        if anchors:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(anchors)
            r_logger.info(f"Card with IP: {get_ip()} has accessed anchors")

        else:
            resp.status = falcon.HTTP_400
            resp.body = "No data found"
            r_logger.info(f"Card with IP: {get_ip()} couldn't find any anchors")


    def on_get_plants(self, req, resp, serverID):

        from Models.Plant import Plant

                 
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


        servers = Server.select(Server, Plant.plant_ID ).join(Plant, on=(Server.server_ID == Plant.server_ID)).where(Server.server_ID == serverID)


        servers = [server for server in servers.dicts()]

        if servers:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(servers)
            r_logger.info(f"Card with IP: {get_ip()} has accessed servers")

        else:
            resp.status = falcon.HTTP_400
            resp.body = "No data found"
            r_logger.info(f"Card with IP: {get_ip()} couldn't find any server")