# -*- coding: utf-8 -*-

def filter_by_name(name):
    def f (message):
        return message['name'] == name
    return f

def create_sensor_actuator_pair(number, has, start_port):
    actuator_name = 'switch_'
    actuator_position = 'pos_'
    sensor_name = 'switch_sensor_'
    sensor_position = 'switch_sensor_pos_'
    for i in range(1, number + 1):
        d = FakeSwitchDriver()
        actuator = Light(has.send_message, d, actuator_name + str(i), actuator_position + str(i))  # lint:ok
        has.add_actuator(actuator)

        sensor = LitSwitch(sensor_name + str(i), sensor_position + str(i), has.send_message)  # lint:ok

        # asociate s1 messages to l1 using in this case sensor name
        has.register_listener(const.SWITCH_SENSOR_ON, actuator, filter_by_name(sensor.name))
        has.register_listener(const.SWITCH_SENSOR_OFF, actuator, filter_by_name(sensor.name))
        print("Actuator {} -- Sensor {}".format(actuator.name,sensor.name))
        # start s1 driver on port 8888
        LitDriver(sensor.start_sensing, '127.0.0.1', start_port + i)


def create_clients(number, start_port):
    import socket
    import random
    import time
    messages = [b"ON", b"OFF"]
    sockets = []
    sleep_times = [0, 1, 0.5]
    for i in range(1,number + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', start_port + i)
        print("client in {}".format(server_address))
        sock.connect(server_address)
        time.sleep(1)
        sockets.append(sock)

    while True:
        message = random.choice(messages)
        client = random.choice(sockets)
        print("Client sending {} to {}".format(message, client.getpeername()))
        client.sendall(message)
        m = client.recv(len(message))
        print("Client received {} -- to sleep".format(m))
        time.sleep(ramdom.choice(sleep_times))


if __name__ == "__main__":

    from domo.domo import HAS
    from domo.actuators.switch import *
    from domo.actuators.light import *
    from domo.sensors.lit_switch import *
    from domo.sensors.lit_switch_driver import *
    import domo.constants as const
    import asyncio
    import concurrent.futures

    has = HAS()
    create_sensor_actuator_pair(2, has, 8888)

    loop = asyncio.get_event_loop()
    try:
        exe = concurrent.futures.ProcessPoolExecutor(max_workers=1)
        exe.submit(create_clients, 2, 8888)
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()