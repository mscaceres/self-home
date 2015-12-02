from domo.actuators.switch.on_off_switch import OnOffSwitch
import domo.constants as const

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



class Light(OnOffSwitch):

    def __init__(self, has, driver, position, name):
        super().__init__(has, driver, position, name)
        self.topic = const.LIGHT