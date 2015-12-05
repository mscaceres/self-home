import enum
from domo.actuators import Actuator
from domo import constants as const

class SwitchState(enum.Enum):
    ON = 0
    OFF = 1


class OnOffSwitch(Actuator):

    def __init__(self, has, driver, position, name):
        super().__init__()
        self.driver = driver
        self.position = position
        self.name = name
        self._state = SwitchState.OFF
        self.has = has
        driver.register_event_handler(self.state)
        self.topic = const.SWITCH

    @property
    def state(self):
        return self._state

    @state.setter
    def set_state(self, new_state):
        if new_state in SwitchState:
            self._state = new_state
            self.has.send_message(self.topic, self.message)
        else:
            raise ValueError("%s not in %s" % (new_state, SwitchState))

    @property
    def message(self):
        return {'id': self.id, 'name': self.name, 'pos': self.position, 'state': self.state}

    def on(self):
        if (self.state == SwitchState.OFF):
            self.driver.on()
            self.state = SwitchState.ON

    def off(self):
        if (self.state == SwitchState.ON):
            self.driver.off()
            self.state = SwitchState.OFF

    def __str__(self):
        return "%s at %s is %s" % (self.name, self.position, self.state.name)
