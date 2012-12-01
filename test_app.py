from Canteen import *

app = Canteen()


@app.add_route('/')
def front_page():
	return 'This is the front page'



app.run_server()

