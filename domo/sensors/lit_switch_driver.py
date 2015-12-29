# -*- coding: utf-8 -*-
import asyncio
import logging

log = logging.getLogger(__name__)


class LitDriver(asyncio.Protocol):

    def __init__(self, cb, host, port):
        self.sensor_cb = cb
        self.loop = asyncio.get_event_loop()
        server = self.loop.create_server(lambda: self, host, port)
        self.server = self.loop.run_until_complete(server)
        self.socket_name = self.server.sockets[0].getsockname()
        log.info('Serving on {}'.format(self.socket_name))

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        log.info('Driver: Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        log.info('{} --> {}: {!r}'.format(self.peername,
                                          self.socket_name, message))
        #log.info('Driver: Send: {!r}'.format(message))
        # self.transport.write(data)
        log.info('Calling driver callback {}'.format(self.sensor_cb.__name__))
        self.sensor_cb(message.strip())

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
