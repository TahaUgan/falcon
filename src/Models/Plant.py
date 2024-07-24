
from Models.Company import Company
from Models.BaseModel import BaseModel
from Models.Token import Token
from Models.Session import Sessions
from Models.Loggers import e_logger, s_logger, r_logger
from Models.Server import Server
from Models.GetIP import get_ip

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
        
        plant = Plant.get(Plant.plant_ID == plantID)
        serverID = plant.server_ID

        
        

        try:

            servers = Server.select().where(Server.server_ID == serverID)

            server = [server for server in servers.dicts()]

        except DoesNotExist as dne:
            resp.status = falcon.HTTP_501
            resp.body = "This plant does not have any Server installed"
            e_logger.error(f"search for not existing server from IP: {get_ip()}")
            print(dne)
            return

        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(server)


        
    