# -*- coding: utf-8 -*-
from domo.sensors import Sensor
from domo.actuators.switch import SwitchState
from domo import constants as const
import asyncio
import logging

log = logging.getLogger(__name__)


class LitSwitch(Sensor):

    def __init__(self, name, position, send_message):
        super().__init__()
        self.name = name
        self.position = position
        self.send_message = send_message
        self.state = SwitchState.OFF
        # maybe a call to configure and register to the hal

    def start_sensing(self, message):
        log.info("New message from driver: {}".format(message))
        self.state = SwitchState[message]
        if self.state == SwitchState.OFF:
            self.send_message(const.SWITCH_SENSOR_OFF, self.message)
        elif self.state == SwitchState.ON:
            self.send_message(const.SWITCH_SENSOR_ON, self.message)
        else:
            pass

    @property
    def message(self):
        return {'id': self.id,
                'name': self.name,
                'pos': self.position,
                'state': self.state}

    def __repr__(self):
        return "%s at %s is %s" % (self.name, self.position, self.state.name)
