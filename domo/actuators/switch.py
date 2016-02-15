import enum
import asyncio
import logging
from domo.actuators import Actuator
from domo import constants as const


log = logging.getLogger(__name__)


class SwitchState(enum.Enum):
    ON = 0
    OFF = 1

# driver shall also be using a loop, so we can switch a task when performing IO
class FakeSwitchDriver:

    def __init__(self, id=None):
        self.id = id

    def on(self):
        log.info("Driver: Turning on a light")

    def off(self):
        log.info("Driver: Turning off a light")


class ToggleSwitch(Actuator):

    TOPIC = const.SWITCH

    def __init__(self, on_message, driver, name, position, id=None, loop=None):
        super().__init__(id=id, on_message=on_message, driver=driver, loop=loop)
        self.position = position
        self.name = name
        self._state = SwitchState.OFF

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state in SwitchState:
            self._state = new_state
            log.info("New state: {}".format(self._state))
            log.info("Sending message: {}".format(self.message))
            self.on_message(self.TOPIC, self.message)
        else:
            raise ValueError("{} not in {}".format(new_state, SwitchState))

    #TODO we should have a module to build and manage messages so we can change it at will.
    @property
    def message(self):
        return {'id': self.id,
                'name': self.name,
                'pos': self.position,
                'state': self.state,
                'type': self.type}

    # If calling driver, then it should be a couroutine???
    def on(self):
        if (self.state == SwitchState.OFF):
            self.driver.on()
            self.state = SwitchState.ON

    def off(self):
        if (self.state == SwitchState.ON):
            self.driver.off()
            self.state = SwitchState.OFF

    def __call__(self, topic, message):
        if message.state == SwitchState.ON:
            self.on()
        elif message.state == SwitchState.OFF:
            self.off()
        else:
            # log error
            pass

    def __repr__(self):
        return "{0} at {1} is {2}".format(self.name, self.position, self.state.name)


class TemporizedSwitch(ToggleSwitch):

    def __init__(self, on_message, driver, name, position, on_time=0, off_time=0, id=None, loop=None):
        super().__init__(on_message=on_message, driver=driver, name=name, position=position, id=id, loop=loop)
        self.on_time = int(on_time)
        self.off_time = int(off_time)

    def _less_than_a_day(self, seconds):
        return seconds < 86400

    def on(self):
        super().on()
        if self.on_time:
            self.loop.call_later(self.on_time, self.off)

    def off(self):
        super().off()
        if self.off_time:
            self.loop.call_later(self.off_time, self.on)

    @property
    def on_time(self):
        return self._on_time

    @on_time.setter
    def on_time(self, seconds):
        if self._less_than_a_day(seconds):
            self._on_time = seconds
        else:
            raise ValueError("Time shall be less than 86400 seconds")

    @property
    def off_time(self):
        return self._off_time

    @off_time.setter
    def off_time(self, seconds):
        if self._less_than_a_day(seconds):
            self._off_time = seconds
        else:
            raise ValueError("Time shall be less than 86400 seconds")
