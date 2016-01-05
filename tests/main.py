# -*- coding: utf-8 -*-
# Used to simulate a house with N actuators and sensors, the actuators used just print
# action and the sensor open a network connection waiting for a stimulus
# When the stimulus arrives, the asyncio loop wake up the corresponing sensor this send
# the event to the event dispacher so the actuators can respond in consecuense.

import logging
import logging.config
from domo.has import HAS
from domo.actuators.switch import *
from domo.actuators.light import *
from domo.sensors.lit_switch import *
from domo.sensors.lit_switch_driver import *
import domo.constants as const
import asyncio
import json

log = logging.getLogger()


def filter_by_name(name):
    def f(message):
        return message['name'] == name
    return f


def create_sensor_actuator_pair(number, has, start_port):
    actuator_name = 'switch_'
    actuator_position = 'pos_'
    sensor_name = 'switch_sensor_'
    sensor_position = 'switch_sensor_pos_'
    for i in range(1, number + 1):
        d = FakeSwitchDriver()
        actuator = Light(has.send_message,
                         d,
                         actuator_name + str(i),
                         actuator_position + str(i))  # lint:ok
        has.add_actuator(actuator)

        sensor = LitSwitch(sensor_name + str(i), sensor_position +
                           str(i), has.send_message)  # lint:ok

        # asociate s1 messages to l1 using in this case sensor name
        has.register_listener(const.SWITCH_SENSOR_ON,
                              actuator, filter_by_name(sensor.name))
        has.register_listener(const.SWITCH_SENSOR_OFF,
                              actuator, filter_by_name(sensor.name))
        # start s1 driver on port 8888
        LitDriver(sensor.on_data, '127.0.0.1', start_port + i)
        log.info("Actuator {} -- Sensor {}".format(actuator.name, sensor.name))


if __name__ == "__main__":
    with open(r"c:\gitrepos\self-home\tests\logs.json") as f:
        c = f.read()
        config = json.loads(c)
    print(config)
    logging.config.dictConfig(config)
    has = HAS()
    create_sensor_actuator_pair(30, has, 8880)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
