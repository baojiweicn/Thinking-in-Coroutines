#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import time
import ujson
import logging
import sys

logger = logging.getLogger('ws_test')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/tmp/test.log',
                    filemode='w')

class ws_sender():
    def __init__(self,index):
        self.index = index
        self._ws = None

    async def get_ws_pool(self):
        if not self._ws:
            session = aiohttp.ClientSession()
            self._ws = await session.ws_connect("ws://0.0.0.0:8000/chat")
        return self._ws

    async def send_str(self,msg):
        res = await self._ws.send_str(msg)
        return res

    async def get_str(self):
        res = await self._ws.receive()
        return res.data

    async def start(self):
        msg =  {"message":time.time(),"user":self.index}
        await self.send_str(ujson.dumps(msg))
        logger.debug(msg)
        asyncio.sleep(3)

class ws_receiver():
    def __init__(self,index):
        self.index = index
        self._ws = None

    async def get_ws_pool(self):
        if not self._ws:
            session = aiohttp.ClientSession()
            self._ws = await session.ws_connect("ws://0.0.0.0:8000/chat")
        return self._ws

    async def send_str(self,msg):
        res = await self._ws.send_str(msg)
        return res

    async def get_str(self):
        res = await self._ws.receive()
        return res.data

    async def start(self):
        start_time = time.time()
        msg = await self.get_str()
        res = ujson.loads(msg)
        current = time.time()
        if current - float(res["message"]) <= 1:
            logger.debug("%s received message in %s"%(self.index,current - float(res["message"])))
            logger.info("receiver %s success" %self.index)
        else:
            logger.error("receiver %s failed" %self.index)

def main(nums):
    loop = asyncio.get_event_loop()

    async def start_test(nums):
        sender = ws_sender(0)
        await sender.get_ws_pool()

        opeators = []
        for i in range(1,nums):
            opeator = ws_receiver(i)
            await opeator.get_ws_pool()
            opeators.append(opeator)

        while True:
            await sender.start()
            for opeator in opeators:
                await opeator.start()

    loop.run_until_complete(start_test(nums))

if __name__ == "__main__":
    args = sys.argv
    nums = int(args[1])
    main(nums)
