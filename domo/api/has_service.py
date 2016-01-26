import json
import asyncio
import logging
from aiohttp import web
from functools import wraps


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def rest_handler(handler_func):
    """
    Allows handlers to return dict.
    Errors are handled and put in json format.
    """
    @wraps(handler_func)
    def wrapper(self, request):
        error_code = None
        try:
            res = yield from handler_func(self, request)
            result = dict(status='OK', result=res)
        except web.HTTPClientError as e:
            log.warning('Http error: %r %r', e.status_code, e.reason,
                        exc_info=True)
            error_code = e.status_code
            result = dict(error_code=error_code,
                          error_reason=e.reason,
                          status='FAILED')
        except Exception as e:
            log.warning('Server error', exc_info=True)
            error_code = 500
            result = dict(error_code=error_code,
                          error_reason='Unhandled exception',
                          status='FAILED')

        assert isinstance(result, dict)
        body = json.dumps(result).encode('utf-8')
        result = web.Response(body=body)
        result.headers['Content-Type'] = 'application/json'
        if error_code:
            result.set_status(error_code)
        return result

    return wrapper


class Rest:

    def __init__(self, has, ip, port):
        self.has = has
        self.ip = ip
        self.port = port
        self.app = web.Application()
        self.app.router.add_route('GET', '/', self.index)
        self.app.router.add_route('POST', '/calculate', self.calculate)


    def start(self):
        self.handler = self.app.make_handler()
        f = self.has.loop.create_server(handler, self.ip, self.port)
        self.srv = self.has.loop.run_until_complete(f)
        log.info('serving on %r', srv.sockets[0].getsockname())

    def shutdown(self):
        log.info('\nBye')
        self.has.loop.run_until_complete(self.handler.finish_connections(1.0))
        self.srv.close()
        self.has.loop.run_until_complete(self.srv.wait_closed())
        self.has.loop.run_until_complete(self.app.finish())

    @asyncio.coroutine
    def index(self, request):
        return web.Response(body=b"Hello, world")

    @rest_handler
    @asyncio.coroutine
    def calculate(self, request):
        data = yield from request.json()
        log.info('Message reveived %r', data)
        return dict(answer=42)


def main():
    rest = Rest(object(), 'localhost', 80)
    rest.start()
    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
       rest.shutdown()
    loop.close()


if __name__ == '__main__':
    main()