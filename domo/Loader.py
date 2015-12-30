# -*- coding: utf-8 -*-
import sqlite3

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

class DBLoader(Loader):

    def __init__(self, db):
        self.db = db

    def _get_actuator_fields(self, actuator_id, conn):
        fields = []
        c = conn.cursor()
        c.execute('select field, value from actuator_fields where actuator_id == ?', (actuator_id,))
        for row in c.fetchall():
            fields.append(dict(row))
        return fields

    def _get_actuator_driver(self, actuator_id, conn):
        c = conn.cursor()
        c.execute('select id, type from actuator_drivers where actuator_id == ?', (actuator_id,))
        driver = c.fetchone()
        if driver is None:
            raise LoaderException("Driver is None for actuator {}".format(actuator_id))
        else:
            driver = dict(driver)
        return driver

    def _get_actuator_driver_fields(self, driver_id, conn):
        fields = []
        c = conn.cursor()
        c.execute('select field, value from actuator_driver_fields where driver_id == ?', (driver_id,))
        for row in c.fetchall():
            fields.append(dict(row))
        return fields

    def load_actuators(self):
        actuators = []
        actuator = {}
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            for row in c.execute("select * from actuators"):
                actuator['id'] = row['id']
                actuator['type'] = row['type']
                actuator['fields'] = self._get_actuator_fields(actuator['id'], conn)
                actuator['driver'] = self._get_actuator_driver(actuator['id'], conn)
                actuator['driver']['fields'] = self._get_actuator_driver_fields(actuator['driver']['ID'], conn)
                actuators.append(actuator)
                actuator = {}
        return actuators

    def load_sensors(self):
        pass

    def load_topics(self):
        pass

if __name__ == "__main__":
    l = DBLoader("domo2.db")
    for a in l.load_actuators():
        print(a)