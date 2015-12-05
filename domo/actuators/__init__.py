import uuid

def id_generator():
    return uuid.uuid1()

class Actuator:

    def __init__(self):
        self.id = id_generator()

    def on(self):
        raise NotImplementedError(self)

    def off(self):
        raise NotImplementedError(self)
