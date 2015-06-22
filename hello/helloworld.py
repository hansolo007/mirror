import webapp2
import logging
import base64
import json
import ast

class MainPage(webapp2.RequestHandler):

	def get(self):
        	self.response.headers['Content-Type'] = 'text/plain'
        	self.response.write('Hello, World!')
	
	def post(self):
		obj = ast.literal_eval(self.request.body)
		logging.info( base64.b64decode(  obj['message']['data']))

app = webapp2.WSGIApplication([
    ('/goo/', MainPage),
], debug=True)
