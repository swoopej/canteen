from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
	response_body = ['%s: %s' % (key, value) for key, value in sorted(environ.items())]
	response_body = ''.join(response_body)

	response_body = ['The beginning\n' + '#' * 20 + '\n', 
					response_body,
					'#' * 20 + '\n',
					'The end\n']

	content_length = 0
	for item in response_body:
		content_length += len(item)

	status = '200 OK'
	response_headers = [('Content_Type', 'text_plain'),
						('Content_Length', str(content_length))]
	start_response(status, response_headers)

	return response_body


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