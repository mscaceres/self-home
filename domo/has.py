import domo.event_dispacher as ed
import ids


class HAS:

    def __init__(self):
        self.actuators = {}
        self.sensors = {}

    def add_actuator(self, actuator):
        self.actuators[actuator.id] = actuator

    def get_actuator(self, id):
        a_id = ids.getId(id)
        return self.actuators[a_id]

    def get_actuators(self):
        return self.actuators.values()

    def add_sensor(self, sensor):
        self.sensors[sensor.id] = sensor

    def get_sensor(self, id):
        s_id = ids.getId(id)
        return self.sensors[s_id]

    def get_sensors(self):
        return self.sensors.values()

    def register_listener(self, topic, listener, message_filter=None):
        ed.subscribe(topic, listener, message_filter)

    def send_message(self, topic, message):
        ed.send_message(topic, message)

    def start(self):
        pass

    def shutdown(self):
        pass
