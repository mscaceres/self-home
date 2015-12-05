__author__ = 'mcaceres'

from domo.actuators.switch.on_off_switch import *
import pytest


@pytest.fixture
def fake_driver():
    class FakeDriver():

        def __init__(self):
            self._on = 0
            self._off = 0
            self._register = 0

        def on(self):
            self._on += 1

        def off(self):
            self._off += 1

        def register_event_handler(self,callback):
            self.callback = callback
            self._register += 1

    return FakeDriver()


@pytest.fixture
def fake_send_message():
    return lambda x,y: x


def test_creating_switch(fake_driver, fake_send_message):
    sw = OnOffSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    assert sw.driver._register == 1
    assert sw.message['name'] == 'sw1'
    assert sw.message['pos'] == 'swpos1'
    assert sw.message['state'] == SwitchState.OFF


def test_switch_on(fake_driver, fake_send_message):
    sw = OnOffSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    sw.on()
    assert fake_driver._on == 1
    assert sw.state == SwitchState.ON
    sw.on()
    assert fake_driver._on == 1

def test_switch_off(fake_driver, fake_send_message):
    sw = OnOffSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    assert sw.state == SwitchState.OFF
    sw.off()
    assert fake_driver._off == 0
    assert sw.state == SwitchState.OFF
    sw.on()
    assert fake_driver._on == 1
    sw.off()
    assert fake_driver._off == 1
    assert sw.state == SwitchState.OFF

def test_switch_callback(fake_driver, fake_send_message):
    sw = OnOffSwitch(fake_send_message, fake_driver, "sw1", "swpos1")
    assert sw.state == SwitchState.OFF
    fake_driver.callback(SwitchState.ON)
    assert sw.state == SwitchState.ON
