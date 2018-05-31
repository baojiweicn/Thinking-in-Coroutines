# -*- coding: utf-8 -*-

import asyncio
import datetime


async def anything(i):
    print(i, datetime.datetime.now())
    await asyncio.sleep(i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(anything(i)) for i in range(1,4)]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            print(*task.result())
    finally:
        loop.close()
        print('close', datetime.datetime.now())