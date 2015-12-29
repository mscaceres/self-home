PRAGMA foreign_keys = ON;

-- ############## ACTUATORS STUFF ##################

CREATE TABLE IF NOT EXISTS ACTUATORS(
    ID INTEGER PRIMARY KEY NOT NULL,
    TYPE TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ACTUATOR_FIELDS(
    ID NUMBER PRIMARY KEY NOT NULL,
    FIELD TEXT NOT NULL,
    VALUE TEXT NOT NULL,
    ACTUATOR_ID NUMBER NOT NULL,
    FOREIGN KEY(ACTUATOR_ID) REFERENCES ACTUATORS(ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ACTUACTOR_DRIVERS(
    ID NUMBER PRIMARY KEY,
    TYPE TEXT NOT NULL,
    ACTUATOR_ID NUMBER NOT NULL,
    FOREIGN KEY(ACTUATOR_ID) REFERENCES ACTUATORS(ID) ON UPDATE CASCADE ON DELETE SET NULL
);

-- ############## SENSOR STUFF ##################

CREATE TABLE IF NOT EXISTS SENSORS(
    ID NUMBER PRIMARY KEY,
    TYPE TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS SENSOR_FIELDS(
    ID NUMBER PRIMARY KEY NOT NULL,
    FIELD TEXT NOT NULL,
    VALUE TEXT NOT NULL,
    SENSOR_ID NUMBER NOT NULL,
    FOREIGN KEY(SENSOR_ID) REFERENCES SENSORS(ID)  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SENSOR_DRIVERS(
    ID NUMBER PRIMARY KEY,
    TYPE TEXT NOT NULL,
    SENSOR_ID NUMBER NOT NULL,
    FOREIGN KEY(SENSOR_ID) REFERENCES SENSORS(ID)  ON UPDATE CASCADE ON DELETE SET NULL
);

-- ############## DISPACHING STUFF ##################

CREATE TABLE IF NOT EXISTS TOPICS(
    NAME TEXT
);

CREATE TABLE IF NOT EXISTS DISPACHING(
    TOPIC_NAME TEXT NOT NULL,
    ACTUATOR_ID NUMBER NOT NULL,
    FILTER_METHOD TEXT NOT NULL
);
