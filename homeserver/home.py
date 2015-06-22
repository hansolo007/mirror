import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from gpi.appspot import GmailGrabber

wsconn = list()
mailGrabber = GmailGrabber()

class MainHandler(tornado.web.RequestHandler):
    	def get(self):
        	self.write("Hello, world")
		for con in wsconn:
			try:
				smsMsg = mailGrabber.getSMS()
				con.write_message(json.dumps(smsMsg))
			except:
				del con
				print "Unexpected error:", sys.exc_info()[0]
	

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    
	def open(self):
		wsconn.append(self)
        	print("WebSocket opened")

    	def on_message(self, message):
		#mailGrabber.main()
       		self.write_message(u"You said: " + message )

    	def on_close(self):
		wsconn.remove(self)
        	print("WebSocket closed")


application = tornado.web.Application([
	(r"/ws", EchoWebSocket),
	(r"/home/(.*)",tornado.web.StaticFileHandler, {"path": "./home/"},),
	(r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()


