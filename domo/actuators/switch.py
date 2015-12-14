import enum
from domo.actuators import *
from domo import constants as const


class SwitchState(enum.Enum):
    ON = 0
    OFF = 1

class FakeSwitchDriver():

    def on(self):
        print("Turning on a light")

    def off(self):
        print("Turning off a light")



class OnOffSwitch(Actuator):

    def __init__(self, send_message, driver, name, position):
        super().__init__()
        self.driver = driver
        self.position = position
        self.name = name
        self._state = SwitchState.OFF
        self.send_message = send_message
        self.topic = const.SWITCH

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state in SwitchState:
            self._state = new_state
            self.send_message(self.topic, self.message)
        else:
            raise ValueError("%s not in %s" % (new_state, SwitchState))

    @property
    def message(self):
        return {'id': self.id,
                'name': self.name,
                'pos': self.position,
                'state': self.state}

    def on(self):
        if (self.state == SwitchState.OFF):
            print(self)
            self.driver.on()
            self.state = SwitchState.ON
            print(self)


    def off(self):
        if (self.state == SwitchState.ON):
            print(self)
            self.driver.off()
            self.state = SwitchState.OFF
            print(self)


    def __call__(self,topic,message):
        if topic == const.SWITCH_SENSOR_ON:
            self.on()
        else:
            self.off()

    def __str__(self):
        return "{0} at {1} is {2}".format(self.name, self.position, self.state.name)


#Maybe this should be an application and run on its own thread...
class TemporizedSwitch(OnOffSwitch):

    def __init__(self, send_message, driver, name, position, on_time, off_time):
        super().__init__(send_message, driver, name, position)
        self.on_time = on_time
        self.off_time = off_time

    def on(self):
        pass

    def off(self):
        pass

