from domo.ids import id_generator

__author__ = 'mcaceres'

class Sensor:

    def __init__(self):
        self.id = id_generator()

    def start(self):
        raise NotImplementedError(self)