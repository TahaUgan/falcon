
from Models.BaseModel import BaseModel
from Utility.Loggers import e_logger, s_logger, r_logger
from Models.User import *


from peewee import *

import falcon
import json

class Company(BaseModel):

    Company_ID = IntegerField(primary_key = True)
    Company_Name = CharField()

    def on_get(self, req, resp):
        headers = req.headers

        id = headers.get("ID")
        name = headers.get("NAME")

        token = headers.get("TOKEN")
        session = headers.get("SESSION")
        
        from Models.Session import Sessions
        from Utility.Token import Token


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
            filters.append(Company.Company_ID == id)
        if name:
            filters.append(Company.Company_Name == name)

        try:
            if filters:
                query = Company.select().where(*filters)
            else:
                query = Company.select()
            
            companies = [company for company in query.dicts()]
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(companies)
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({"error": "Internal Server Error"})
            e_logger.error(f"GET /companies => {str(e)}")


    def on_get_plants(self, req, resp ,companyID):
        

        headers = req.headers
        
        token = headers.get("TOKEN")
        session = headers.get("SESSION")

        if not token or not session:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": "Missing authenticative data"})
            e_logger.error("Missing authenticative data")
            return
        
        from Models.Session import Sessions
        from Utility.Token import Token


        if not Token.check_token(token) or not Sessions.check_session(session):
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({"error": "You don't have the authority to do so"})
            e_logger.error("Unauthorized access attempt")
            return



        from Models.Plant import Plant
        plants = Plant.select(Plant).where(Plant.company_ID == companyID)

        
        plants = [plant for plant in plants.dicts()]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(plants)







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

        filters = []
        
        if id:
            filters.append(Company.Company_ID == id)
        if name:
            filters.append(Company.Company_Name == name)


        if filters:
            Company.delete().where(*filters)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps("Company/ies has been removed")
            r_logger.info(f"Companies has been removed with filter: {filters[0]}, IP: {get_ip}")
        else:
            resp.status = falcon.HTTP_400
            resp.body = "No company found with these/this filters"
            e_logger.info(f"Failed company remove attempt, no company found, IP: {get_ip}")


        
