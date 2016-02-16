import enum
import collections
import domo.constants as const
import domo.messages


class AlarmState(enum.Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    RINGING = 2


class ZoneState(enum.Enum):
    OFF = 0
    ON = 1


class AlarmZone:

    def __init__(self, name):
        self.name = name
        self.state = ZoneState.ON
        self.sensors = []

    def __contains__(self, sensor_name):
        return any(sensor_name == sensor.name for sensor in self.sensors)


class Alarm:
    TOPIC = const.ALARM

    def __init__(self, has, key=None):
        self.has = has
        self.sensors = []
        self.actuators = []
        self.state = AlarmState.DEACTIVATED
        self.zones = {}
        self.key = key

    def add_sensor(self, sensor, zone_name=None):
        # add verification to check if sensor is part of HAS
        self.has.register_listener(const.PRESENCE, self, domo.messages.filter_by_name(sensor.name))
        if zone_name is not None:
            if zone_name in self.zones:
                zone = self.zones[zone_name]
                zone.sensors.append(sensor)
            else:
                zone = AlarmZone(zone_name)
                zone.sensors.append(sensor)
                self.zones[zone_name] = zone
        else:
            self.sensors.append(sensor)

    def add_actuator(self, actuator, act_callable):
        # add verification to check if actuator is part of HAS
        self.actuators.append((actuator, act_callable))

    def activate_zone(self, *zone_names):
        for name in zone_names:
            self.zones[name].state = ZoneState.ON

    def de_activate_zone(self, *zone_names):
        for name in zone_names:
            self.zones[name].state = ZoneState.OFF

    def activate_alarm(self):
        self.state = AlarmState.ACTIVATED

    def de_activate_alarm(self, passw):
        if self.key == passw and self.state is AlarmState.RINGING:
            self.state = AlarmState.DEACTIVATED
            # turn off horns.. (what other actions)

    def do_emergency_actions(self, message):
        self.state = AlarmState.RINGING
        for actuator, act_callable in self.actuators:
            act_callable()

    def __call__(self, topic, message):
        if self.state == AlarmState.ACTIVATED:
            if any(sensor.name == message.name for sensor in self.sensors) or \
            any(zone.state is ZoneState.ON and message.name in zone for zone in self.zones.values()):
                self.do_emergency_actions()

