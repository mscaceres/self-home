import abc
import domo.ids as ids
import domo.utils
from collections import namedtuple


__all__ = ['lit_switch', 'lit_switch_driver']

class Sensor(metaclass=abc.ABCMeta):

    def __init__(self, id=None):
        self.id = ids.get_id(id)
        self.on_message = None

    @abc.abstractmethod
    def on_data(self, message):
        pass


class SensorDriver(metaclass=abc.ABCMeta):

    def __init__(self, id=None, cb=None):
        self.id = id
        self.on_data = cb


SensorData = namedtuple('SensorData','cls, id, driver, on_message, fields')
SensorDriverData = namedtuple('SensorData','cls, id, cb, fields')

class SensorFactory:

    @classmethod
    def _build_kwargs(cls, id, on_message, fields):
        kwargs = {}
        kwargs['id'] = id
        kwargs['on_message'] = on_message
        kwargs.update(fields)
        return kwargs

    @classmethod
    def from_tuple(cls, sensor_data):
        cls_name, id, driver, on_message, fields = sensor_data
        cls_obj = domo.utils.find_class(__package__, cls_name)
        kwargs = cls._build_kwargs(id, on_message, fields)
        obj = cls_obj(**kwargs)
        driver = driver._replace(cb=obj.on_data)
        SensorDriverFactory.from_tuple(driver)
        return obj


class SensorDriverFactory:

    @classmethod
    def _build_kwargs(cls, id, cb, fields):
        kwargs = {}
        kwargs['id'] = id
        kwargs['cb'] = cb
        kwargs.update(fields)
        return kwargs

    @classmethod
    def from_tuple(cls, driver_data):
        cls_name, id, cb, fields = driver_data
        cls_obj = domo.utils.find_class(__package__, cls_name)
        kwargs = cls._build_kwargs(id, cb, fields)
        obj = cls_obj(**kwargs)
        return obj
