# -*- coding: utf-8 -*-
import asyncio

class LitDriver(asyncio.Protocol):


    def __init__(self, cb, host, port):
        self.sensor_cb = cb
        self.loop = asyncio.get_event_loop()
        server = self.loop.create_server(lambda: self, host, port)
        self.server = self.loop.run_until_complete(server)
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Driver: Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Driver: Data received: {!r}'.format(message))
        print('Driver: Send: {!r}'.format(message))
        self.transport.write(data)
        self.sensor_cb(message.strip())

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())




