# -*- coding: utf-8 -*-

import asyncio
import datetime


async def anything(i):
    print(i, datetime.datetime.now())
    await asyncio.sleep(i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(anything(3))
    try:
        result = loop.run_until_complete(task)
        print(*result)
    finally:
        loop.close()
        print('close', datetime.datetime.now())