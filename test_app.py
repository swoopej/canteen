from Canteen import *

app = Canteen()


@app.add_route('/')
def front_page():
	return 'This is the front page'

@app.add_route('/hello/<user>/')
def hello_sir(user):
	return 'Top of the morning to you ' + str(user)

@app.add_route('goodbye/<user>/')
def goodday_sir(user):
	return 'Good day to you ' + str(user)

app.run_server()

