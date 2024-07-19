from Models.User import User
from Models.Device import Device
from Models.Room import Room
from Models.Log_In_Out import Login, Logout

import falcon




app = falcon.App()



user_resource = User()
app.add_route('/users', user_resource)

room_resource = Room()
app.add_route('/rooms', room_resource)
app.add_route('/rooms/{room_ID}/users', room_resource, suffix = 'users')


device_resource = Device()
app.add_route('/devices', device_resource)

login_resource = Login()
app.add_route('/login', login_resource)

logout_resource = Logout()
app.add_route('/logout', logout_resource)




if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('', 8001, app) as httpd:
        print('Serving on port 8001...')
        httpd.serve_forever()

