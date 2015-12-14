from domo.actuators.switch import ToggleSwitch
import domo.constants as const

class Light(ToggleSwitch):

    def __init__(self, has, driver, position, name):
        super().__init__(has, driver, position, name)
        self.topic = const.LIGHT