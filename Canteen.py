from wsgiref.simple_server import make_server
from cgi import escape
from urlparse import parse_qs
from rule import Rule
import re
import cgitb
cgitb.enable()


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
		self.environ = {} if environ is None else environ
		self.start = start_response

		path = self.parse_path(environ['PATH_INFO'])

		if path:
			response_body = path() #calls the function in url-routing dict
			status = "200 OK"
		else:
			response_body = "That is an unknown path"
			status = "404 Not Found"

		response_headers = [('Content_Type', 'text/html'),
							('Content_Length', str(len(response_body)))]
		start_response(status, response_headers)
		return [response_body]

	def parse_path(self, path):
		for route in self.routes:
			if route.path == path:
				return route.endpoint
		else:
			return None

	def add_route(self, path, method= 'GET'):
		def decorator(f):
			args = self.add_url(path, f)
			return f(*args)
		return decorator 	

	def add_url(self, path, view_func):
		new_rule = Rule(path, view_func)
		args = new_rule.get_args()
		self.routes.append(new_rule)
		return args



if __name__ == "__main__":
	app = Canteen()
	app.run_server()


