from wsgiref.simple_server import make_server
from cgi import escape
from urlparse import parse_qs
import cgitb
cgitb.enable()

html = """
<html>
<body>
	<form method="post" action="parsing_post.wsgi">
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

	#the environ variable CONTENT_LENGTH may be empty or missing
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	#when the request method is POST the query string will be sent in
	#the HTTP request body which is passed by the WSGI server in the file
	#like wsgi.input environment varible
	request_body = environ['wsgi.input'].read(request_body_size)

	#parses query string into a dictionary containing lists as values
	d = parse_qs(request_body)

	#this idiom issues a list containing a default value
	age = d.get('age', [''])[0] #returns the first age value
	hobbies = d.get('hobbies', [])

	#escape '&', '<' and '>' in string to HTML-safe sequence
	age = escape(age)
	hobbies = [escape(hobby) for hobby in hobbies]

	response_body = html % (age or 'Empty',
						', '.join(hobbies or ['No Hobbies']))

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
httpd.serve_forever()