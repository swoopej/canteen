from wsgiref.simple_server import make_server
from cgi import escape
from urlparse import parse_qs
import cgitb
cgitb.enable()

html = """
<html>
<body>
	<form method="get" action="parsing_get.wsgi">
	  <p>
	    Age: <input type="text" name="age">
	  </p>
	  <p>
	    Hobbies:
	    <input name="hobbies" type="checkbox" value="software"> Software
	    <input name="hobbies" type="checkbox" value="tuning"> Auto Tuning
	  </p>
	  <p>
	    <input type="submit" value="Submit">
	  </p>
	</form>
	<p>
	  Age: %s<br>
	  Hobbies: %s
	</p>
</body>
</html>"""


def simple_app(environ, start_response):
	status = None

	if environ['PATH_INFO'] == '/':
		response_body = construct_body(environ)
		status = '200 OK'
	else:
		response_body = "That is an unknown path"
		status = "404 Not Found"


	response_headers = [('Content_Type', 'text_plain'),
						('Content_Length', str(len(response_body)))]
	start_response(status, response_headers)
	return [response_body]
	
	#def router(rule):
	#	def decorator(f):

def construct_body(environ):
	
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

#instantiate the wsgi server
#receives request, passes to wsgi app
#send app's response to client
httpd = make_server(
	'localhost', 
	8051,
	simple_app
	)

#wait for single request, serve it and quit
httpd.serve_forever()