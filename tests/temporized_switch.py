# -*- coding: utf-8 -*-
from domo.actuators.switch import *
import asyncio

send_message = lambda x, y: True
d = FakeSwitchDriver()
s = TemporizedSwitch(send_message, d, 'temp1', 'pos1', 5, 5)

loop = asyncio.get_event_loop()

loop.call_soon(s.on)
loop.run_forever()
loop.close()


