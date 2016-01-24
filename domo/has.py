import domo.event_dispacher as ed
import ids
import asyncio


class HAS:

    def __init__(self):
        self.actuators = {}
        self.actuators_by_type = {}
        self.sensors = {}
        self.loop = asyncio.get_event_loop()

    def add_actuator(self, actuator):
        self.actuators[actuator.id] = actuator
        self.actuators_by_type[actuator.type] = actuator

    def get_actuator(self, id):
        a_id = ids.get_id(id)
        return self.actuators[a_id]

    def get_actuators(self):
        return self.actuators.values()

    def add_sensor(self, sensor):
        self.sensors[sensor.id] = sensor

    def get_sensor(self, id):
        s_id = ids.get_id(id)
        return self.sensors[s_id]

    def get_sensors(self):
        return self.sensors.values()

    def register_listener(self, topic, listener, message_filter=None):
        ed.subscribe(topic, listener, message_filter)

    def send_message(self, topic, message):
        ed.send_message(topic, message)

    def start(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.close()
        return 0

    def shutdown(self):
        self.loop.close()
        return 0
