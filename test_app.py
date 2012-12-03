from Canteen import *

app = Canteen()


@app.add_route('/')
def front_page():
	return 'This is the front page'

@app.add_route('/hello/')
def hello_sir():
	return 'Top of the morning to you '



app.run_server()

