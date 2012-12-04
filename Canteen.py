from wsgiref.simple_server import make_server
from cgi import escape
from urlparse import parse_qs
from rule import Route
import re
import cgitb
#cgitb.enable()


class Canteen:

	def __init__(self):
		self.routes = []

	def run_server(self):
		#instantiate the wsgi server
		#receives request, passes to wsgi app
		#send app's response to client
		httpd = make_server(
			'localhost', 
			8051,
			self.wsgi_app
			)

		httpd.serve_forever()



	def wsgi_app(self, environ, start_response):
		'''
		called by the server with the environ dict and the start_response function
		
		environ must contain CGI/WSGI variables like PATH_INFO, QUERY_STRING, etc. 

		start_response must be called to start the http response.  

		This function will
		return the response body as an iterable.
		'''


		self.environ = {} if environ is None else environ
		self.start = start_response

		print '\n\npath info: ', environ['PATH_INFO']
		path, args = self.route_request(environ['PATH_INFO'], environ['QUERY_STRING'])

		if path:
			response_body = path(*args) #unpacks the arg dict returned from route_request
			status = "200 OK"
		else:
			response_body = "That is an unknown path"
			status = "404 Not Found"

		response_headers = [('Content_Type', 'text/html'),
							('Content_Length', str(len(response_body)))]

		start_response(status, response_headers)
		return [response_body]

	def route_request(self, path_info, query_string):
		'''   
		path parameter and query string are from the environ dict
		'''

		path = path_info
		args = parse_qs(query_string) #returns a dict 

		arg_list = []
		if args:
			for k, v in args.items():
				arg_list.append(v)


		for route in self.routes:
			if route.path == path:
				return route.endpoint, arg_list
		else:
			return None


	def add_route(self, path, method= 'GET'):
		'''decorates a user supplied function by adding path to self.routes'''
		def decorator(f):
			args = self.create_route(path, f)
			return f(*args)
		return decorator 	

	def create_route(self, path, view_func):
		new_route = Route(path, view_func)
		args = new_route.get_args()
		self.routes.append(new_route)
		return args





if __name__ == "__main__":
	app = Canteen()
	app.run_server()


