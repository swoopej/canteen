from wsgiref.simple_server import make_server
from cgi import escape
from urlparse import parse_qs
import cgitb
cgitb.enable()


class Canteen:

	def __init__(self):
		self.routes = {}

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
		tokens = path.split('/')
		if path in self.routes:
			return self.routes[path]
		else:
			return None

	def add_route(self, path):
		def decorator(f):
			self.add_url(path, f)
			return f
		return decorator 	

	def add_url(self, path, view_func):
		self.routes[path] = view_func


	def construct_body(self, environ):
		
		#returns a dictionary containing lists as values
		d = parse_qs(environ['QUERY_STRING'])
	 
		#this idiom issues a list containing a default value
		age = d.get('age', [''])[0] #returns the first age value
		hobbies = d.get('hobbies', [])

		#escape '&', '<' and '>' in string to HTML-safe sequence
		age = escape(age)
		hobbies = [escape(hobby) for hobby in hobbies]

		return html % (age or 'Empty',
						', '.join(hobbies or ['No Hobbies']))


if __name__ == "__main__":
	app = Canteen()
	app.run_server()


