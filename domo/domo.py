import domo.event_dispacher as ed
import uuid


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

    def register_listener(self, topic, listener, message_filter=None):
        ed.subscribe(topic, listener, message_filter)

    def send_message(self, topic, message):
        ed.send_message(topic, message)


