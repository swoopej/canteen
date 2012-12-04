import re

class Rule:

	def __init__(self, path, func):
		self.path = path
		self.endpoint = func
		self.args = []
		tokens = self.path.split('/')
		for token in tokens:
			if re.match('<\w+>', token):
				self.args.append(token.strip('<').strip('>'))

	def get_args(self):
		return self.args
