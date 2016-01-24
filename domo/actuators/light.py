from domo.actuators.switch import ToggleSwitch
import domo.constants as const

class Light(ToggleSwitch):

    def __init__(self, on_message, driver, position, name, id=None, loop=None):
        super().__init__(on_message=on_message, driver=driver, name=name, position=position, id=id, loop=loop)
        self.topic = const.LIGHT