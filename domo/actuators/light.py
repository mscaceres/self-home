from domo.actuators.switch import ToggleSwitch
import domo.constants as const

class Light(ToggleSwitch):

    def __init__(self, send_message, driver, position, name, id=None):
        super().__init__(send_message, driver, name, position,id=id)
        self.topic = const.LIGHT