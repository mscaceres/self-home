# -*- coding: utf-8 -*-
import sys
import logging


log = logging.getLogger(__name__)

class Usage(Exception):

    def __init__(self, msg):
        self.msg = msg


def parse_args(args):
    pass

def start(options):

    # type and kwarfs shall be taken from a Json config file or something
    l = loader.getFrom('db', kwargs)
    for actuator_data in l.load_actuators_data():
            has.add_actuator(Actuator.from_tuple(actuator_data))

    for sensor_data in loader.load_sensor_data()
            has.add_sensor(Sensor.from_tuple(sensor_data))

def shutdown():
    pass


def main(args=None):
    if args is None:
        args = sys.argv
    try:
        options = parse_args(args)
        start(options)
        return 0
    except Usage as ex:
        print(ex.msg)
        print("For help use --help")
    except Exception as ex:
        log.exeption(ex)
        return 1
    finally:
        shutdown()



if __name__ == "__main__":
    sys.exit(main())