
from Models.Company import Company
from Models.BaseModel import BaseModel
from Utility.Token import Token

from Utility.Loggers import e_logger, s_logger, r_logger
from Models.Server import Server
from Utility.GetIP import get_ip
from peewee import *

import falcon
import json

class Plant(BaseModel):

    plant_ID = IntegerField(primary_key=True)
    plant_Name = CharField()
    company_ID = ForeignKeyField(Company, db_column = 'Company_ID', backref='company')
    server_ID = ForeignKeyField(Server, db_column = 'Server_ID', backref='Server')

    def on_get(self, req, resp):

        headers = req.headers
        
        id = headers.get("ID")
        name = headers.get("NAME")
        company_id = headers.get("COMPANY_ID")
        server_id = headers.get("SERVER_ID")

        token = headers.get("TOKEN")
        session = headers.get("SESSION")


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
            filters.append(Plant.plant_ID == id)
        if name:
            filters.append(Plant.plant_Name == name)
        if company_id:
            filters.append(Plant.company_ID == company_id)
        if server_id:
            filters.append(Plant.server_ID == server_id)



        if filters:
            plants = Plant.select().where(*filters)
        else:
            plants = Plant.select()


        plants = [plant for plant in plants.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(plants)





    def on_get_servers(self, req, resp, plantID):

        headers = req.headers

        token = headers.get("TOKEN")
        session = headers.get("SESSION")


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
        
        plant = Plant.get(Plant.plant_ID == plantID)
        serverID = plant.server_ID

        
        

        try:

            servers = Server.select().where(Server.server_ID == serverID)

            server = [server for server in servers.dicts()]

        except DoesNotExist as dne:
            resp.status = falcon.HTTP_501
            resp.body = "This plant does not have any Server installed"
            e_logger.error(f"search for not existing server from IP: {get_ip()}")
            return

        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(server)


    def on_delete(self, req, resp):
    
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

        id = headers.get("ID")
        name = headers.get("NAME")

        if not id:
            resp.status = falcon.HTTP_400
            resp.body = "Can't delete with body"
            return

        from Models.Plant import Plant
        from Models.Place import Place
        from Models.Server import Server

        filters = []

        if id:
            filters.append(Plant.plant_ID == id)
        if name:
            filters.append(Plant.plant_Name == name)

        if filters:
            plants = Plant.select().where(*filters)

            if not plants:
                resp.status = falcon.HTTP_400
                resp.body = f"This Plant does not exist"
                e_logger.error(f"Attempt on deleting inexistant plant, from IP: {get_ip()}")
                return

            for plant in plants:
                # Delete associated places
                places = Place.select().where(Place.Plant_ID == plant.plant_ID)
                for place in places:
                    # Delete associated servers for each place
                    place.plant_ID = None
                    place.save()            
                    
                plant.delete_instance()

            resp.status = falcon.HTTP_200
            resp.body = json.dumps("Plant/ies, associated places, and servers have been removed")
            r_logger.info(f"Plants, associated places, and servers have been removed with filter: {filters[0]}, IP: {get_ip()}")
        else:
            resp.status = falcon.HTTP_400
            resp.body = "No plant found with these/this filters"
            e_logger.info(f"Failed plant remove attempt, no plant found, IP: {get_ip()}")

