from Canteen import *
import pdb

app = Canteen()


@app.add_route('/index', methods = ['GET', 'POST'])
def front_page():
	print 'request method ', request.method
	return 'This is the front page'

@app.add_route('/hello/<user>/')
def hello_sir(user):
	return 'Top of the morning to you ' + str(user)

@app.add_route('goodbye/<user>/', methods = ['GET', 'POST'])
def goodday_sir(user):
	print 'request method: ', request.method
	return 'Good day to you ' + str(user)

@app.add_route('/yolo/<userone>/', methods = ['GET', 'POST'])
def yolo(userone):
	return 'user one: ' + str(userone)

app.run_server()

