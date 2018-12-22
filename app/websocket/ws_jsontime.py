import json
from datetime import datetime
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

class EchoApplication(WebSocketApplication):
    def on_open(self):
        print("Connection opened")

# Try sending a JSON encoded message with timestamp
    def on_message(self, message):
        d = datetime.now()
        ds = d.strftime("%d/%m/%Y %H:%M:%S")
        data = json.dumps({ 'time': ds, 'text': 'Hello there!' })
        self.ws.send(data)

    def on_close(self, reason):
        print(reason)

WebSocketServer(
    ('', 8000),
    Resource({'/': EchoApplication})
).serve_forever()
