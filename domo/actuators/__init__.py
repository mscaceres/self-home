from domo.ids import id_generator

class Actuator:

    def __init__(self):
        self.id = id_generator()

    def on(self):
        raise NotImplementedError(self)

    def off(self):
        raise NotImplementedError(self)
