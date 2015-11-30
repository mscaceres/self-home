import uuid
import enum
import domo.event_dispacher as ed
import domo.constants as const


class HAS:

    def __init__(self):
        self.actuators = {}

    def add_actuator(self, actuator):
        self.actuators[actuator.id] = actuator

    def get_actuator(self, id):
        uu_id = uuid.UUID(id)
        return self.actuators[uu_id]

    def get_actuators(self):
        return self.actuators.values()

    def register_listener(self, topic, listener, message_filter):
        ed.subscribe(topic, listener, message_filter)

    def send_message(self, topic, message):
        ed.send_message(topic, message)


def id_generator():
    return uuid.uuid1()


class Actuator:

    def __init__(self):
        self.id = id_generator()

    def on(self):
        raise NotImplementedError(self)

    def off(self):
        raise NotImplementedError(self)


class Sensor:

    def read(self):
        raise NotImplementedError


class Driver:
    """Low level implementation of an actuator"""

    def get_state(self):
        pass

    def on(self):
        print("Turning on")

    def off(self):
        print("Turning off")

    def register_event_handler(self, callback):
        self.event_callback = callback


class SwitchState(enum.Enum):
    ON = 0
    OFF = 1


class Switch(Actuator):

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
    def state(self, new_state):
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


class Light(Switch):

    def __init__(self, has, driver, position, name):
        super().__init__(has, driver, position, name)
        self.topic = const.LIGHT
