# -*- coding: utf-8 -*-
import sqlite3
import importlib

class FactoryError(Exception):

    def __init__(self, cls, kwargs, org_msg):
        self.cls = cls
        self.kwarfs = kwargs
        self.org_msg = org_msg

    def __repr__(self):
        msg = """{}
        for class {} in module {}
        with fields {}""".format(self.org_msg,
                                 self.cls.__name__,
                                 self.cls.__module__,
                                 self.kwargs)
        return msg


class SensorFactory:

    def __init__(self):
        self.id = None
        self.type = None
        self.fields = None
        self.driver = None


class DriverFactory:

    def __init__(self):
        self.id = None
        self.type = None
        self.fields = None

class ActuatorFactory:

    ACTUATOR_PACKAGE = "domo.actuators"

    def __init__(self):
        self.id = None
        self.type = None
        self.fields = None
        self.driver = None

    def _find_class(self):
        base_package = importlib.import_module(self.ACTUATOR_PACKAGE)
        for mdl_name in base_package.__all__:
            child_mdl = importlib.import_module("{}.{}".format(self.ACTUATOR_PACKAGE, mdl_name))
            try:
                cls = getattr(child_mdl, self.type)
            except AttributeError:
                pass
            else:
                return cls

    def _build_kwargs(self):
        kwargs = {}
        kwargs['id'] = self.id
        # I need to update these two attributes, once I have a better way
        kwargs['driver'] = None
        kwargs['send_message'] = None
        kwargs.update(self.fields)
        return kwargs

    def get_actuator(self):
        cls = self._find_class()
        kwargs = self._build_kwargs()
        try:
            obj = cls(**kwargs)
        except TypeError as t:
            raise FactoryError(cls, kwargs, str(t))
        else:
            return obj


class LoaderException(Exception):
    pass

class Loader:

    def load_actuators(self):
        raise NotImplementedError(self)

    def load_sensors(self):
        raise NotImplementedError(self)

    def load_message_topics(self):
        raise NotImplementedError(self)

# Another option if we are not going to query by attributes is to save a pickled object
# by defining an adapter and converter functions to sqlite3. Then we just save and read
# the object.
# If quering attributes is important then we need to switch to SQLAlchemy

# At the moment I do not believe we will need a heavy usage of DB, just in case of shutdown
# Everything shall be in memory...
# How do we support HA???

class DBLoader(Loader):

    def __init__(self, db):
        self.db = db

    def _get_fields(self, tbl, tbl_key, tbl_value, conn):
        fields = []
        c = conn.cursor()
        query = "select field, value from {} where {} == ?".format(tbl, tbl_key)
        c.execute(query,(tbl_value,))
        for row in c.fetchall():
            fields.append(dict(row))
        return fields

    def _get_driver(self, tbl, tbl_key, tbl_value, conn):
        c = conn.cursor()
        query = "select id, type from {} where {} == ?".format(tbl, tbl_key)
        c.execute(query, (tbl_value,))
        try:
            did, dtype = c.fetchone()
        except TypeError:
            raise LoaderException("Driver is None for {} {}".format(tbl, tbl_value))
        return (did, dtype)

    def load_actuators(self):
        actuators = []
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select id, type from actuators"):
                actuator = ActuatorFactory()
                actuator.id= row['id']
                actuator.type = row['type']
                actuator.fields = self._get_fields("actuator_fields", "actuator_id", actuator.id, conn)

                driver = DriverFactory()
                driver.id, driver.type = self._get_driver("actuator_drivers", "actuator_id", actuator.id, conn)
                driver.fields  = self._get_fields("actuator_driver_fields","driver_id", driver.id, conn)
                actuator.driver = driver

                actuators.append(actuator)
        return actuators

    def load_sensors(self):
        sensors = []
        sensor = {}
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select id, type from sensors"):
                sensor = SensorFactory()
                sensor.id = row['id']
                sensor.type = row['type']
                sensor.fields = self._get_fields("sensor_fields", "sensor_id", sensor.id, conn)
                driver = DriverFactory
                driver.id, driver.type = self._get_driver("sensor_drivers", "sensor_id", sensor.id, conn)
                driver.fields = self._get_fields("sensor_driver_fields","driver_id", driver.id, conn)
                sensor.driver = driver
                sensors.append(sensor)
        return sensors


    def load_topics(self):
        pass

if __name__ == "__main__":
    l = DBLoader("domo2.db")
    for a in l.load_actuators():
        print(a)

    print("="*50)

    for a in l.load_sensors():
        print(a)