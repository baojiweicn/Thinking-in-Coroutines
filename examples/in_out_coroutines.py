task = loop.create_task(coro())
result = loop.run_until_complete(coro())

task = loop.create_task(coro())
result = await coro()