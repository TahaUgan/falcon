
from Models.BaseModel import BaseModel
from Utility.Loggers import e_logger, s_logger, r_logger
from Models.User import *
from Utility.GetIP import get_ip


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

        if not id:
            resp.status = falcon.HTTP_400
            resp.body = "Can't delete with body"
            return


        from Models.Plant import Plant


        filters = []
        
        if id:
            filters.append(Company.Company_ID == id)
        if name:
            filters.append(Company.Company_Name == name)


        if filters:
            
            companies = Company.select().where(*filters)

            if not companies:
                resp.status = falcon.HTTP_400
                resp.body = f"This Company does not exist"
                e_logger.error(f"Attempt on deleting inexistant company, from IP: {get_ip()}")
                return

            for company in companies:
                company.delete_instance()

            resp.status = falcon.HTTP_200
            resp.body = json.dumps("Company/ies has been removed")
            r_logger.info(f"Companies has been removed with filter: {filters[0]}, IP: {get_ip()}")
        else:
            resp.status = falcon.HTTP_400
            resp.body = "No company found with these/this filters"
            e_logger.info(f"Failed company remove attempt, no company found, IP: {get_ip()}")


        
    def on_post_migrate(self, req, resp, companyID):
        
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

        newCompID = headers.get("COMPANYID")
        newCompName = headers.get("COMPANYNAME")

        try:

            company = Company.create(Company_ID = newCompID, Company_Name = newCompName)
            company.save()

        except IntegrityError as ie:
            resp.status = falcon.HTTP_400
            resp.body = f"This company already exists"
            e_logger.error(f"Tried to create an existing company from IP: {get_ip()}")
            return



        from Models.Histories.Plant_history import Plant_history
        from Models.Plant import Plant

        try:

            plant_histories = Plant_history.select().where(Plant_history.Company_ID == companyID, Plant_history.Is_Last == 'Last')

        except DoesNotExist as dne:
            resp.status = falcon.HTTP_400
            resp.body = "No Such record has found"
            e_logger.error(f"Migration attempt with non-existing plant record, IP: {get_ip()}")
            return

        for plant_history in plant_histories:

            target_plant_ID = plant_history.Plant_ID

            try:

                plant = Plant.select().where(Plant.plant_ID == target_plant_ID).get()

            except DoesNotExist as dne:
                resp.status = falcon.HTTP_400
                resp.body = "This plant may have been deleted"
                e_logger.error(f"Record exists but plant does not, plantID: {target_plant_ID}, IP: {get_ip()}")
                return

            if plant.Company_ID: #means that, this plant is in use already
                resp.status = falcon.HTTP_226
                resp.body = "This plant already has a Company that it is connected to"
                e_logger.error(f"Tried to assing a in-use plant to a cmopany")
                return

            if not newCompID:
                resp.status = falcon.HTTP_400
                resp.body = f"Missing new Company ID"
                e_logger.error(f"Attempt on creating a new company without new Company ID, ID: {newCompID}")
                return

        
            
    
            plant.Company_ID = newCompID
            plant.save()


        
        resp.status = falcon.HTTP_201
        resp.body = f"Company succesfully created"
        r_logger.info(f"Created a company with ID: {newCompID} from IP: {get_ip()}")



