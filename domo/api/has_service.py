import json
import asyncio
import logging
import collections
import enum
import uuid
from aiohttp import web
from functools import wraps


log = logging.getLogger(__name__)


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.name
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


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
        body = json.dumps(result, cls=EnumEncoder).encode('utf-8')
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
        self.srv = None
        self.handler = None
        self.app.router.add_route('GET', '/has_service/api/v1.0/status', self.get_status)
        self.app.router.add_route('GET', '/has_service/api/v1.0/status/{id}', self.get_status)
        self.app.router.add_route('GET', '/has_service/api/v1.0/status/{type}', self.get_status_by_type)
        # self.app.router.add_route('GET', '/has_service/api/v1.0/status/{type}/{id}', self.get_status_by_type)
        # self.app.router.add_route('POST', '/has_service/api/v1.0/actuator', self.create_actuator)
        # self.app.router.add_route('POST', '/has_service/api/v1.0/sensor', self.create_sensor)
        # self.app.router.add_route('PUT', '/has_service/api/v1.0/actuator/{id}', self.update_actuator)
        # self.app.router.add_route('PUT', '/has_service/api/v1.0/sensor/{id}', self.update_sensor)


    def start(self):
        self.handler = self.app.make_handler()
        f = self.has.loop.create_server(self.handler, self.ip, self.port)
        self.srv = self.has.loop.run_until_complete(f)
        log.info('serving on %r', self.srv.sockets[0].getsockname())

    def shutdown(self):
        log.info('\nBye')
        self.has.loop.run_until_complete(self.handler.finish_connections(1.0))
        self.srv.close()
        self.has.loop.run_until_complete(self.srv.wait_closed())
        self.has.loop.run_until_complete(self.app.finish())

    @rest_handler
    @asyncio.coroutine
    def get_status(self, request):
        devices = collections.defaultdict(list)
        item_id = request.match_info.get('id', None)
        if item_id is None:
            for actuator in  sorted(self.has.get_actuators(), key=lambda a: a.type):
                devices[actuator.name] = actuator.message
        else:
            actuator = self.has.get_actuator(item_id)
            devices[actuator.name] = actuator.message
        return devices

    @rest_handler
    @asyncio.coroutine
    def get_status_by_type(self, request):
        devices = collections.defaultdict(list)
        item_type = request.match_info.get('type', None)
        for actuator in self.has.get_actuators_by_type(item_type):
            devices[actuator.name] = actuator.message
        return devices


    @rest_handler
    @asyncio.coroutine
    def calculate(self, request):
        data = yield from request.json()
        log.info('Message reveived %r', data)
        return dict(answer=42)

