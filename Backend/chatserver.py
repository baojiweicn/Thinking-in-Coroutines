#########################################################################################################
#   Create new chatserver.py use Sanic                                                                  #
#   Start command:                                                                                      #
#       gunicorn chatserver:app --bind 0.0.0.0:8000 -w 4 --worker-class sanic.worker.GunicornWorker     #
#   Make sure redis open                                                                                #
#########################################################################################################

import ujson
import asyncio
import logging
import uuid

import asyncio_redis
from sanic import Sanic, response

app = Sanic(__name__)
app.static('/','./')
logger = logging.getLogger('chat')
class Redis:
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(host='localhost', port=6379, poolsize=500)
        return self._pool

redis = Redis()

@app.listener('before_server_start')
async def before_srver_start(app, loop):
    app.broker = await redis.get_redis_pool()

@app.middleware('response')
async def cors_res(request, response):
    request.app.broker.close()

@app.route("/index")
async def index(request):
    return response.redirect("index.html")

async def subscribe(request,ws):
    subscriber = await request.app.broker.start_subscribe()
    await subscriber.subscribe(['room1'])
    while True:
        msg = await subscriber.next_published()
        logger.info(msg)
        await ws.send(msg.value)

async def publish(request,ws):
    userid = uuid.uuid4()
    while True:
        data = await ws.recv()
        data = ujson.loads(data)
        data["user"] = userid.hex
        logger.info(data)
        data = ujson.dumps(data)
        await request.app.broker.publish('room1',data)

@app.websocket('/chat')
async def chat(request, ws):
    await asyncio.gather(publish(request,ws),subscribe(request,ws))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

#################
#   old code    #
#################
#import json
#from gevent.pywsgi import WSGIServer
#from geventwebsocket.handler import WebSocketHandler
#from geventwebsocket.resource import Resource, WebSocketApplication
#class MemoryBroker():
#    def __init__(self):
#        self.sockets = {}
#
#    def subscribe(self, key, socket):
#        if key not in self.sockets:
#            self.sockets[key] = set()
#
#        if socket in self.sockets[key]:
#            return
#
#        self.sockets[key].add(socket)
#
#    def publish(self, key, data):
#        for socket in self.sockets[key]:
#            socket.on_broadcast(data)
#
#    def unsubscribe(self, key, socket):
#        if key not in self.sockets: return
#
#        self.sockets[key].remove(socket)
#
#
#broker = MemoryBroker()
#
#class Chat(WebSocketApplication):
#
#    def on_open(self, *args, **kwargs):
#        self.userid = uuid.uuid4()
#        broker.subscribe('room1', self)
#
#    def on_close(self, *args, **kwargs):
#        broker.unsubscribe('room1', self)
#
#    def on_message(self, message, *args, **kwargs):
#        if not message: return
#
#        data = json.loads(message)
#        data['user'] = self.userid.hex
#        broker.publish('room1', data)
#
#    def on_broadcast(self, data):
#        print(data)
#        self.ws.send(json.dumps(data))
#
#
#def index(environ, start_response):
#    start_response('200 OK', [('Content-type','text/html')])
#    html = open('index.html', 'rb').read()
#    return [html]
#
#application = Resource([
#    ('^/chat', Chat),
#    ('^/', index)
#])
#
#if __name__ == '__main__':
    #WSGIServer('{}:{}'.format('0.0.0.0', 8000), application, handler_class=WebSocketHandler).serve_forever()
