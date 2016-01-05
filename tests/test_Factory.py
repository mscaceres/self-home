# -*- coding: utf-8 -*-
import pytest
import domo.loader

@pytest.fixture
def bad_params():
    af = domo.loader.ActuatorFactory()
    af.id = 1
    af.type = "ToggleSwitch"
    af.fields = {'bla':'key1', 'ble':'kitchen'}
    return af

@pytest.fixture
def bad_type():
    af = domo.loader.ActuatorFactory()
    af.id = 1
    af.type = "NonExistingType"
    af.fields = {'bla':'key1', 'ble':'kitchen'}
    return af


@pytest.fixture
def ts():
    af = domo.loader.ActuatorFactory()
    af.id = 1
    af.type = "ToggleSwitch"
    af.fields = {'name':'key1', 'position':'kitchen'}
    return af

@pytest.fixture
def lg():
    af = domo.loader.ActuatorFactory()
    af.id = 1
    af.type = "Light"
    return af


def test_find_class(ts, lg):
    import domo.actuators.switch
    import domo.actuators.light
    cls = ts._find_class()
    assert (cls == domo.actuators.switch.ToggleSwitch)
    cls2 = lg._find_class()
    assert (cls2 == domo.actuators.light.Light)


def test_get_actuators(ts):
    import domo.actuators.switch
    actuator = ts.get_actuator()
    assert type(actuator) is domo.actuators.switch.ToggleSwitch
    assert actuator.name == "key1"
    assert actuator.position == "kitchen"


def test_actuator_wrong_params(bad_params):
    import domo.loader
    with pytest.raises(domo.loader.FactoryParamsError):
        obj = bad_params.get_actuator()


def test_wrong_type(bad_type):
    import domo.loader
    with pytest.raises(domo.loader.FactoryClassError):
        obj = bad_type.get_actuator()