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

		path, args, method = self.route_request(environ)
		print '\n\npath: ', path


		if path and args:
			response_body = path(*args) #unpacks the arg dict returned from route_request
			status = "200 OK"
		elif path:
			response_body = path() #no args
			status = "200 OK"
		else:
			response_body = "That is an unknown path"
			status = "404 Not Found"

		response_headers = [('Content_Type', 'text/html'),
							('Content_Length', str(len(response_body)))]

		start_response(status, response_headers)
		return [response_body]

	def route_request(self, environ):

		path = environ['PATH_INFO']
		request_method = environ['REQUEST_METHOD']
		query_string =  environ['QUERY_STRING']

		#the environ variable CONTENT_LENGTH may be empty or missing
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0
			
		wsgi_input = environ['wsgi.input'].read(request_body_size)
		post_data = parse_qs(wsgi_input)

		#parses url query string if present and method is get
		arg_list = []
		if request_method == 'GET' and query_string:
			arg_list = self.parse_args(query_string)


		for route in self.routes:
			if route.path == path and request_method in route.get_methods():
				return route.endpoint, arg_list, request_method
		else:
			return None, None, None

	def parse_args(self, query_string):
		'''parses the query string in url if present'''
		arg_list = []
		args = parse_qs(query_string)
		for k, v in args.items():
			arg_list.append(v)

		return arg_list


	def add_route(self, path, methods= 'GET'):
		'''decorates a user supplied function by adding path to self.routes'''
		def decorator(f):
			args = self.create_route(path, f, methods)
			return f(*args)
		return decorator 	

	def create_route(self, path, view_func, methods):
		new_route = Route(path, view_func, methods)
		args = new_route.get_args()
		self.routes.append(new_route)
		return args





if __name__ == "__main__":
	app = Canteen()
	app.run_server()


