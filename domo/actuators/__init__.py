import domo.ids as ids
import abc
import domo.utils
from collections import namedtuple


__all__ = ["switch", "light"]

_this_package = __package__


class Actuator(metaclass=abc.ABCMeta):

    def __init__(self, id=None, driver=None, on_message=None):
        self.id = ids.get_id(id)
        self.driver = driver
        self.on_message = on_message

    @abc.abstractmethod
    def on(self):
        pass

    @abc.abstractmethod
    def off(self):
        pass


class ActuatorDriver(metaclass=abc.ABCMeta):

    def __init__(self, id=None):
        self.id = ids.get_id(id)


# Classes used to decouple fromwhere the data is to be readen and how to create the target object
# So we read data from Json, DB, CSV, etc to this middle namedtuple.
# Then we create Actuators from them.

ActuatorTuple = namedtuple("ActuatorTuple", "cls, driver, on_message, id, fields")
ActuatorDriverTuple = namedtuple("ActuatorDriverTuple", "cls, id, fields")


class ActuatorDriverFactory:

    @classmethod
    def from_tuple(cls, driver_tuple):
        cls_name, id, fields = driver_tuple
        fields.update({'id':id})
        cls_obj = domo.utils.find_class(_this_package, cls_name)
        obj = cls_obj(**fields)
        return obj


class ActuatorFactory:

    @classmethod
    def _build_kwargs(cls, driver, on_message, id, other_fields):
        kwargs = {}
        kwargs['driver'] = ActuatorDriverFactory.from_tuple(driver)
        # This parameter is needed to send message to the HOUSE so other actuators con react on.
        kwargs['on_message'] = on_message
        kwargs['id'] = id
        kwargs.update(other_fields)
        return kwargs

    @classmethod
    def from_tuple(cls, actuator_tuple):
        cls_name, driver, on_message, id, other_fields = actuator_tuple
        cls_obj = domo.utils.find_class(_this_package, cls_name)
        kwargs = cls._build_kwargs(driver, on_message, id, other_fields)
        obj = cls_obj(**kwargs)
        return obj
