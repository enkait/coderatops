from tornado import websocket
from tornado import web
from tornado import ioloop
import threading

# Single threaded, inefficient, boring implementation
class PubSub:
    store = {}
    lock = threading.RLock()

    def pub(self, msg):
        self.lock.acquire()
        for handler in self.store.values():
            handler(msg)
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
    def open(self, name):
        print "Opened"
        self.pub_sub = pub_sub_finder.get(name)
        self.pub_sub.sub(self, self.publish)
        #print arg
        #print "WebSocket opened"
        #print dir(self)
        #print self.get_arguments("wut2")
        #print self.request
        #print dir(self.request)

    def on_message(self, message):
        print "Message arrived"
        self.write_message(u"You said: " + message)

    def publish(self, message):
        print "Publishing"
        self.write_message(message)

    def on_close(self):
        print "WebSocket closed"
        self.pub_sub.unsub(self)

app = web.Application([(r'/ws/(.*)', PubSubWebSocket)])

if __name__ == '__main__':
    print "Starting"
    app.listen(6379)
    ioloop.IOLoop.instance().start()
