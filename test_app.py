from Canteen import *

app = Canteen()


@app.add_route('/index', methods = ['GET', 'POST'])
def front_page():
    print 'request method ', request.method
    return 'This is the front page'

@app.add_route('/hello/<str:user>/')
def hello_sir(user):
    return 'Top of the morning to you ' + str(user)

@app.add_route('/goodbye/<str:user>/', methods = ['GET', 'POST'])
def goodday_sir(user):
    print 'request method: ', request.method
    return 'Good day to you ' + str(user)

@app.add_route('/yolo/<str:userone>/<str:usertwo>', methods = ['GET', 'POST'])
def yolo(userone, usertwo):
    return 'user one: ' + str(userone) + '\nuser two: ' + str(usertwo)

@app.add_route('/soloyolo/<int:id>', methods = ['GET', 'POST'])
def solo_yolo(solo):
    response = 'hello there ' + str(solo)
    return response

app.run_server()

