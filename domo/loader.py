# -*- coding: utf-8 -*-
import sqlite3
import abc
import domo.actuators
import domo.sensors


class LoaderException(Exception):
    pass


def getFrom(source_type, *args):
    try:
        cls = source_type.upper()+'Loader'
        loader_cls = globals()[cls]
        return loader_cls(*args)
    except KeyError as err:
        pass
#       ConfigError("Loading objects from {} is not supported".format(cls))
    except TypeError as err:
        pass
#       ConfigError("Parameters are missing for class {}, provided {}".format(cls,str(kwargs)))


class Loader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_actuators_data(self):
        pass

    @abc.abstractmethod
    def load_sensors_data(self):
        pass

    @abc.abstractmethod
    def load_message_topics(self):
        pass

# Another option if we are not going to query by attributes is to save a pickled object
# by defining an adapter and converter functions to sqlite3. Then we just save and read
# the object.
# If quering attributes is important then we need to switch to SQLAlchemy

# At the moment I do not believe we will need a heavy usage of DB, just in case of shutdown
# Everything shall be in memory...
# How do we support HA???

# Once we have a Page to create the Sensors, Actuators, et all. we should be saving the objects to DB
# using pickle instead of all this crap.

class DBLoader(Loader):

    def __init__(self, db):
        self.db = db

    def _get_fields(self, tbl, tbl_key, tbl_value, conn):
        fields = {}
        c = conn.cursor()
        query = "select field, value from {} where {} == ?".format(tbl, tbl_key)
        c.execute(query, (tbl_value,))
        for row in c.fetchall():
            fields.update({row['field']: row['value']})
        c.close()
        return fields

    def _get_driver(self, tbl, tbl_key, tbl_value, conn):
        c = conn.cursor()
        query = "select id, type from {} where {} == ?".format(tbl, tbl_key)
        c.execute(query, (tbl_value,))
        d_id, d_type = c.fetchone()
        c.close()
        return d_id, d_type

    def load_actuators_data(self):
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select id, type from actuators"):
                id = row['id']
                cls = row['type']
                fields = self._get_fields("actuator_fields", "actuator_id", id, conn)
                d_id, d_cls = self._get_driver("actuator_drivers", "actuator_id", id, conn)
                d_fields = self._get_fields("actuator_driver_fields","driver_id", d_id, conn)
                driver = domo.actuators.ActuatorDriverTuple(d_cls, d_id, d_fields)
                yield domo.actuators.ActuatorTuple(cls, driver, None, id, None, fields)
            c.close()

    def load_sensors_data(self):
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select id, type from sensors"):
                id = row['id']
                cls = row['type']
                fields = self._get_fields("sensor_fields", "sensor_id", id, conn)
                d_id, d_cls = self._get_driver("sensor_drivers", "sensor_id", id, conn)
                d_fields = self._get_fields("sensor_driver_fields","driver_id", d_id, conn)
                driver = domo.sensors.SensorDriverData(d_cls, d_id, None, d_fields)
                yield domo.sensors.SensorData(cls, id, driver, None, fields)
            c.close()

    def load_message_topics(self):
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select topic_name, actuator_id, filter_method  from dispaching"):
                yield (row['topic_name'], row['actuator_id'], row['filter_method'])
            c.close()


# TODO> I need to add some UT for this module
if __name__ == "__main__":
    l = DBLoader("./domo/domo2.db")
    for a in l.load_actuators_data():
        print(a)

    print("="*50)

    for a in l.load_sensors_data():
        print(a)