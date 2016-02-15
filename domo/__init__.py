import os

__doc__ = "Domotics for your home"
__version__ = 1.0
__author__ = "Mauro Caceres"
__email__ = "mauro.caceres@gmail.com"


class FromEnv:
    """ Look for env_var in the environment at each access, if the variable is not present then return a default_value.
    If a value is set it is used as the new default value.
    Precedence is
        1) environment value
        2) default value, that can be set.
    """
    def __init__(self, env_var, default_value):
        self.var = env_var
        self.value = default_value

    def __get__(self, obj, type):
        try:
            return os.environ[self.var]
        except KeyError:
            return self.value

    def __set__(self, obj, value):
        self.value = value


def from_env(cls):
    for k, v in cls.__dict__.items():
        if k.startswith('__'): continue
        if callable(v): continue
        setattr(cls, k, FromEnv(k, v))
    return cls


@from_env
class Configs:
    LOADER_SOURCE = 'DB'
    LOADER_DB_PATH = "/home/mauro/gitrepos/self-home/sql/domo2.db"
    LOGS_CONFIG = r"/home/mauro/gitrepos/self-home/resources/logs.json"
    REST_IP = "localhost"
    REST_PORT = "9999"
