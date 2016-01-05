import domo.ids as ids
import abc
import domo.utils
from collections import namedtuple


__all__ = ["switch", "light"]


class Actuator(metaclass=abc.ABCMeta):

    def __init__(self, id=None):
        self.id = ids.get_id(id)
        self.driver = None
        self.on_message = None

    @abc.abstractmethod
    def on(self):
        pass

    @abc.abstractmethod
    def off(self):
        pass

class ActuatorDriver(metaclass=abc.ABCMeta):

    def __init__(self, id=None):
        self.id = ids.get_id(id)


# Class used to decouple fromwhere the data is to be readen and how to create the object
# So we read data from Json, DB, CSV, etc to this objects.
# Then we create Actuators from them.
ActuatorData = namedtuple("ActuatorData", "cls, driver, on_message, id, fields")
ActuatorDriverData = namedtuple("ActuatorDriverData", "cls, id, fields")


class ActuatorDriverFactory:

    @classmethod
    def from_tuple(cls, driver_data):
        cls_name, id, fields = driver_data
        fields.update({'id':id})
        cls_obj = domo.utils.find_class(__package__, cls_name)
        obj = cls(**fields)
        return obj


class ActuatorFactory:

    @classmethod
    def _build_kwargs(cls, driver, on_message, id, other_fields):
        kwargs = {}
        kwargs['driver'] = ActuatorDriverFactory.from_data(driver)
        # This parameter is needed to send message to the HOUSE so other actuators con react on.
        kwargs['on_message'] = on_message
        kwargs['id'] = id
        kwargs.update(other_fields)
        return kwargs

    @classmethod
    def from_tuple(cls, actuator_data):
        cls_name, driver, on_message, id, other_fields = actuator_data
        cls_obj = domo.utils.find_class(__package__, cls_name)
        kwargs = cls._build_kwargs(driver, on_message, id, other_fields)
        obj = cls_obj(**kwargs)
        return obj
