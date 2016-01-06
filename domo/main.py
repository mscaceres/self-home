# -*- coding: utf-8 -*-
import sys
import logging
import domo.has
import domo.loader
import domo.actuators
import domo.sensors

log = logging.getLogger(__name__)

class Usage(Exception):

    def __init__(self, msg):
        self.msg = msg


def parse_args(args):
    pass


def start(options, home):

    # type and kwarfs shall be taken from a Json config file or something
    l = domo.loader.getFrom('db', kwargs)
    for actuator_tuple in l.load_actuators_data():
            actuator_tuple = actuator_tuple._replace(on_message=has.send_message)
            home.add_actuator(domo.actuators.ActuatorFactory.from_tuple(actuator_tuple))

    for sensor_tuple in l.load_sensor_data():
            sensor_tuple = sensor_tuple._replace(on_message=has.send_message)
            home.add_sensor(domo.sensors.SensorFactory.from_tuple(sensor_tuple))

    home.start()


def shutdown(home):
    home.shutdown()


def main(args=None):
    if args is None:
        args = sys.argv
    try:
        options = parse_args(args)
        home = domo.has.HAS()
        start(options, home)
        return 0
    except Usage as ex:
        print(ex.msg)
        print("For help use --help")
    except Exception as ex:
        log.exeption(ex)
        return 1
    finally:
        shutdown(home)



if __name__ == "__main__":
    sys.exit(main())