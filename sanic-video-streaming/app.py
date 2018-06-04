import asyncio
import os
import logging
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

import aredis
from sanic import Sanic, response

app = Sanic(__name__)
app.static('/','./templates')
logger = logging.getLogger('chat')


class Redis:
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = aredis.StrictRedis(host='localhost', port=6379)
        return self._pool


redis = Redis()


@app.listener('before_server_start')
async def before_srver_start(app, loop):
    app.broker = await redis.get_redis_pool()


@app.route("/index")
async def index(request):
    return response.redirect("index.html")


async def subscribe(request,ws):
    subscriber = request.app.broker.pubsub()
    await subscriber.subscribe(['room1'])
    msg = await subscriber.get_message()
    while True:
        msg = await subscriber.get_message()
        data = msg['data']
        logger.info(msg)
        try:
            data = data.decode()
        except Exception:
            pass
        await ws.send(data)


async def publish(request,ws):
    camera = Camera()
    while True:
        frame = camera.get_frame()

        await request.app.broker.publish('room1', frame)


@app.websocket('/chat')
async def chat(request, ws):
    await asyncio.gather(publish(request,ws),subscribe(request,ws))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)