# -*- coding: utf-8 -*-
import asyncio

class LitDriver(asyncio.Protocol):


    def __init__(self, cb, host, port):
        self.sensor_cb = cb
        self.loop = asyncio.get_event_loop()
        server = self.loop.create_server(lambda: self, host, port)
        self.server = self.loop.run_until_complete(server)
        self.socket_name = self.server.sockets[0].getsockname()
        print('Serving on {}'.format(self.socket_name))

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Driver: Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        print("="*30)
        message = data.decode()
        print('{} --> {}: {!r}'.format(self.peername, self.socket_name, message))
        #print('Driver: Send: {!r}'.format(message))
        #self.transport.write(data)
        self.sensor_cb(message.strip())

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())




