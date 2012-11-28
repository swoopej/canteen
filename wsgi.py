from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
	response_body = 'HELLO MY FRIEND'

	
	status = '200 OK'
	response_headers = [('Content_Type', 'text_plain'),
						('Content_Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]


#instantiate the wsgi server
#receives request, passes to wsgi app
#send app's response to client
httpd = make_server(
	'localhost', 
	8051,
	simple_app
	)

#wait for single request, serve it and quit
httpd.handle_request()