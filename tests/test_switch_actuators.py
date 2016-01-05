__author__ = 'mcaceres'

from domo.actuators.switch import *
import pytest


@pytest.fixture
def fake_driver():
    class FakeDriver():

        def __init__(self):
            self._on = 0
            self._off = 0

        def on(self):
            self._on += 1

        def off(self):
            self._off += 1

    return FakeDriver()


@pytest.fixture
def fake_send_message():
    return lambda x, y: x


def test_creating_toggleswitch(fake_driver, fake_send_message):
    sw = ToggleSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    assert sw.message['name'] == 'sw1'
    assert sw.message['pos'] == 'swpos1'
    assert sw.message['state'] == SwitchState.OFF


def test_toggleswitch_on(fake_driver, fake_send_message):
    sw = ToggleSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    sw.on()
    assert fake_driver._on == 1
    assert sw.state == SwitchState.ON
    sw.on()
    assert fake_driver._on == 1


def test_toggleswitch_off(fake_driver, fake_send_message):
    sw = ToggleSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    assert sw.state == SwitchState.OFF
    sw.off()
    assert fake_driver._off == 0
    assert sw.state == SwitchState.OFF
    sw.on()
    assert fake_driver._on == 1
    sw.off()
    assert fake_driver._off == 1
    assert sw.state == SwitchState.OFF


def test_creating_temporizedswitch(fake_driver, fake_send_message):
    sw = TemporizedSwitch(send_message=fake_send_message,
                      driver=fake_driver,
                      name="temp1",
                      position="temppos1",
                      on_time=10,
                      off_time=10)
    assert sw.message['name'] == 'temp1'
    assert sw.message['pos'] == 'temppos1'
    assert sw.message['state'] == SwitchState.OFF
    assert sw.on_time == 10
    assert sw.off_time == 10


def test_creating_temporizedswitch_default_values(fake_driver, fake_send_message):
    sw = TemporizedSwitch(send_message=fake_send_message,
                      driver=fake_driver,
                      name="temp1",
                      position="temppos1")
    assert sw.message['name'] == 'temp1'
    assert sw.message['pos'] == 'temppos1'
    assert sw.message['state'] == SwitchState.OFF
    assert sw.on_time == 0
    assert sw.off_time == 0


def test_temporizedswitch_on_time_exception(fake_driver, fake_send_message):
    with pytest.raises(ValueError):
        sw = TemporizedSwitch(send_message=fake_send_message,
                          driver=fake_driver,
                          name="temp1",
                          position="temppos1",
                          on_time=86400,
                          off_time=10)



def test_temporizedswitch_off_time_exception(fake_driver, fake_send_message):
    with pytest.raises(ValueError):
        sw = TemporizedSwitch(send_message=fake_send_message,
                          driver=fake_driver,
                          name="temp1",
                          position="temppos1",
                          on_time=10,
                          off_time=864001)