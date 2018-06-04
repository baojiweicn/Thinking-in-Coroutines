#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import time

def main():
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()

    async def before_start(session):
        ws = await session.ws_connect("ws://0.0.0.0:8000/chat")
        return ws

    ws = loop.run_until_complete(before_start(loop))
    local_vars = locals()
    local_vars['ws'] = ws

    def send_str(s):
        async def run(s):
            res = await ws.send_str(s)
            return res
        res = loop.run_until_complete(run(s))
        return res

    local_vars['send_str'] = send_str
    try:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed()
        ipshell()
    except ImportError:
        import code
        pyshell = code.InteractiveConsole(locals=local_vars)
        pyshell.interact()

if __name__ == "__main__":
    main()
