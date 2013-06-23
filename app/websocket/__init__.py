import flask
 
import tornado
import tornado.websocket
import tornado.wsgi
 
app = flask.Flask(__name__)
 
@app.route('/')
def index():
    return flask.render_template('index.html')
 
class ChatWebSocket(tornado.websocket.WebSocketHandler):
    clients = []
 
    def open(self):
        ChatWebSocket.clients.append(self)
 
    def on_message(self, message):
        for client in ChatWebSocket.clients:
            client.write_message(message)
 
    def on_close(self):
        ChatWebSocket.clients.remove(self)
 
tornado_app = tornado.web.Application([
    (r'/websocket', ChatWebSocket),
    (r'.*', tornado.web.FallbackHandler, {'fallback': tornado.wsgi.WSGIContainer(app)})
])
 
tornado_app.listen(5000)
tornado.ioloop.IOLoop.instance().start()
