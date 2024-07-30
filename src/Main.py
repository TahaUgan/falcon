
from Models.User import User
from Models.Card import Card
from Models.Room import Room
from Models.Log_In_Out import Login, Logout
from Models.Company import Company
from Models.Plant import Plant
from Models.Server import Server
from Models.Place import Place
from Models.Anchor import Anchor
from Models.Histories.Room_logs import Room_logs


import falcon





app = falcon.App()



user_resource = User()
app.add_route('/users', user_resource)
app.add_route('/users/{userID}/anchors', user_resource, suffix = 'anchors')


card_resource = Card()
app.add_route('/cards', card_resource)

login_resource = Login()
app.add_route('/login', login_resource)

logout_resource = Logout()
app.add_route('/logout', logout_resource)

company_resource = Company()
app.add_route('/companies', company_resource)
app.add_route('/companies/{companyID}/plants', company_resource, suffix = 'plants')
app.add_route('/companies/{companyID}/migration', company_resource, suffix='migrate')

plant_resource = Plant()
app.add_route('/plants', plant_resource)
app.add_route('/plants/{plantID}/servers', plant_resource, suffix='servers')

server_resource = Server()
app.add_route('/servers', server_resource)
app.add_route('/servers/{serverID}/anchors', server_resource, suffix= 'anchors')
app.add_route('/servers/{serverID}/plants', server_resource, suffix='plants')

place_resource = Place()
app.add_route('/places', place_resource)
app.add_route('/places/{placeID}/rooms', place_resource, suffix='rooms')

room_resource = Room()
app.add_route('/rooms', room_resource)
app.add_route('/rooms/cards', room_resource, suffix='cards_rooms')
app.add_route('/rooms/users/count', room_resource, suffix='users_count')

anchor_resource = Anchor()
app.add_route('/anchors', anchor_resource)
app.add_route('/anchors/cards', anchor_resource, suffix='matching_cards')


room_change_resource = Room_logs()
app.add_route('/change-room/{userID}', room_change_resource, suffix='change_room')
app.add_route('/room/{roomID}/past', room_change_resource, suffix='past_users')



if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('', 8001, app) as httpd:
        print('Serving on port 8001...')
        httpd.serve_forever()


