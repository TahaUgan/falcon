
import falcon
import Resource






app = falcon.App()



# Add routes
user_resource = Resource.User()
app.add_route('/users', user_resource)

room_resource = Resource.Room()
app.add_route('/rooms', room_resource)

device_resource = Resource.Device()
app.add_route('/devices', device_resource)

login_resource = Resource.Login()
app.add_route('/login', login_resource)

logout_resource = Resource.Logout()
app.add_route('/logout', logout_resource)




if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('', 8001, app) as httpd:
        print('Serving on port 8001...')
        httpd.serve_forever()







