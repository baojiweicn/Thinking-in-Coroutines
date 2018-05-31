# -*- coding: utf-8 -*-

from asyncio import futures


class Task(futures.Future):
    def __init__(self, loop=None):
        super().__init__(loop=loop)
        self.count = 0
        self._loop.call_soon(self._step)

    def _step(self):
        try:
            result = next(self._coro)
        except StopIteration as exc:
            self.set_result(exc.value)
        except BaseException as exc:
            self.set_exception(exc)
        else:
            self.count += 1
            self._loop.call_soon(self._step)