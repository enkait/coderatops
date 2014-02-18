from tornado import websocket
from tornado import web
from tornado import ioloop
import threading
import json

# Single threaded, inefficient, boring implementation
class PubSub:
    store = {}
    lock = threading.RLock()

    def pub(self, type, payload):
        self.lock.acquire()
        message = json.dumps({
            "type": type,
            "payload": payload,
        })
        for handler in self.store.values():
            handler(message)
        self.lock.release()

    def sub(self, key, handler):
        self.lock.acquire()
        self.store[key] = handler
        self.lock.release()

    def unsub(self, key):
        self.lock.acquire()
        del self.store[key]
        self.lock.release()

class PubSubFinder:
    store = {}
    lock = threading.RLock()

    def get(self, name):
        self.lock.acquire()
        if not name in self.store:
            self.store[name] = PubSub()
        result = self.store[name]
        self.lock.release()
        return result

pub_sub_finder = PubSubFinder()

class PubSubWebSocket(websocket.WebSocketHandler):
    def open(self, auth_token):
        print "Opened"
        self.pub_sub = pub_sub_finder.get(auth_token)
        self.pub_sub.sub(self, self.publish)

    def on_message(self, message):
        print "Message arrived", message
        #self.write_message(u"You said: " + message)

    def publish(self, message):
        print "Publishing:", message
        self.write_message(message)

    def on_close(self):
        print "WebSocket closed"
        self.pub_sub.unsub(self)

app = web.Application([(r'/ws/(.*)', PubSubWebSocket)])

if __name__ == '__main__':
    print "Starting"
    app.listen(6379)
    ioloop.IOLoop.instance().start()
