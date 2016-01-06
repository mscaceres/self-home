# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def ts():
    import domo.actuators
    dt = domo.actuators.ActuatorDriverTuple(cls="FakeSwitchDriver",
                                            id=1,
                                            fields={})

    at = domo.actuators.ActuatorTuple(cls="ToggleSwitch",
                                      driver=dt,
                                      on_message=None,
                                      id=1,
                                      fields={"name": "key1", "position": "kitchen"})
    return at


@pytest.fixture
def missing_fields():
    import domo.actuators
    dt = domo.actuators.ActuatorDriverTuple(cls="FakeSwitchDriver",
                                            id=1,
                                            fields={})

    at = domo.actuators.ActuatorTuple(cls="ToggleSwitch",
                                      driver=dt,
                                      on_message=None,
                                      id=1,
                                      # exclude name parameter
                                      fields={"position": "kitchen"})
    return at

def test_find_class():
    import domo.utils
    import domo.actuators.switch
    import domo.actuators.light
    cls = domo.utils.find_class("domo.actuators", "ToggleSwitch")
    assert (cls == domo.actuators.switch.ToggleSwitch)
    cls2 = domo.utils.find_class("domo.actuators", "Light")
    assert (cls2 == domo.actuators.light.Light)


def test_non_existing_class():
    "if the class does not exists a AttributeError shall be raised"
    import domo.utils
    with pytest.raises(AttributeError):
        cls = domo.utils.find_class("domo.actuators", "NonExistingClass")


def test_get_actuators(ts):
    import domo.actuators.switch
    import domo.actuators
    actuator = domo.actuators.ActuatorFactory.from_tuple(ts)
    assert type(actuator) is domo.actuators.switch.ToggleSwitch
    assert actuator.name == "key1"
    assert actuator.position == "kitchen"


def test_missing_abstract_methods():
    import domo.actuators

    class f(domo.actuators.Actuator):
        pass
    with pytest.raises(TypeError):
        obj = f()


def test_not_fail_silently(missing_fields):
    import domo.actuators
    with pytest.raises(Exception):
        a = domo.actuators.ActuatorFactory.from_tuple(missing_fields)