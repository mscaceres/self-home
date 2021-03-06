# -*- coding: utf-8 -*-
from domo.sensors import Sensor
from domo.actuators.switch import SwitchState
from domo import constants as const
import asyncio
import logging

log = logging.getLogger(__name__)


class LitSwitch(Sensor):

    def __init__(self, name, position, on_message, id=None):
        super().__init__(id=id)
        self.name = name
        self.position = position
        self.on_message = on_message
        self.state = SwitchState.OFF
        # maybe a call to configure and register to the hal

    def on_data(self, message):
        log.info("New message from driver: {}".format(message))
        self.state = SwitchState[message]
        self.on_message(const.SWITCH, self.message)


    @property
    def message(self):
        return {'id': self.id,
                'name': self.name,
                'pos': self.position,
                'state': self.state,
                'type': self.type}

    def __repr__(self):
        return "%s at %s is %s" % (self.name, self.position, self.state.name)
