# -*- coding: utf-8 -*-
import sys
import logging
import logging.config
import json
import domo.has
import domo.loader
import domo.actuators
import domo.sensors
import domo.messages


log = logging.getLogger(__name__)

class Usage(Exception):

    def __init__(self, msg):
        self.msg = msg


def parse_args(args):
    pass


def start(options, home):

    # type and kwargs shall be taken from a Json config file or something
    l = domo.loader.getFrom('db', db="/home/mauro/gitrepos/self-home/domo/domo2.db")

    for actuator_tuple in l.load_actuators_data():
            actuator_tuple = actuator_tuple._replace(on_message=home.send_message, loop=home.loop)
            home.add_actuator(domo.actuators.ActuatorFactory.from_tuple(actuator_tuple))

    for sensor_tuple in l.load_sensors_data():
            sensor_tuple = sensor_tuple._replace(on_message=home.send_message)
            home.add_sensor(domo.sensors.SensorFactory.from_tuple(sensor_tuple))

    for topic, id, filter_func_str in l.load_message_topics():
        actuator = home.get_actuator(id)
        filter_func = domo.messages.get_filter_func(filter_func_str)
        home.register_listener(topic=topic, listener=actuator, message_filter=filter_func)

    return home.start()


def shutdown(home):
    return home.shutdown()


def main(args=None):
    if args is None:
        args = sys.argv
    try:
        with open(r"/home/mauro/gitrepos/self-home/resources/logs.json") as f:
            c = f.read()
            config = json.loads(c)
        logging.config.dictConfig(config)
        options = parse_args(args)
        home = domo.has.HAS()
        start(options, home)
    except Usage as ex:
        print(ex.msg)
        print("For help use --help")
        return 1
    except Exception as ex:
        log.exception(stack_info=True)
        return 1
    finally:
        return shutdown(home)



if __name__ == "__main__":
    sys.exit(main())