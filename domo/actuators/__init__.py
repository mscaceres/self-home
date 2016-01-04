import domo.ids as ids


__all__ = ["switch", "light"]

class Actuator:

    def __init__(self, id=None):
        self.id = ids.get_id(id)

    def on(self):
        raise NotImplementedError(self)

    def off(self):
        raise NotImplementedError(self)
