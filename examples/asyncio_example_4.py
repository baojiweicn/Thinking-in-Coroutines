# -*- coding: utf-8 -*-

import asyncio
import datetime


async def anything(i):
    print(i, datetime.datetime.now())
    await asyncio.sleep(i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(2, loop.stop)
    for i in range(1, 4):
        loop.create_task(anything(i))
    try:
        loop.run_forever()
    finally:
        loop.close()
        print('close', datetime.datetime.now())
