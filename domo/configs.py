import os

class FromEnv:
    def __init__(self,var ,default_value):
        self.var = var
        self.value = default_value

    def __get__(self, instance, ):
        try:
            return os.environ[self.var]
        except KeyError:
            return self.value


LOADER_SOURCE = FromEnv('LOADER_SOURCE', "DB")
LOADER_DB_PATH = "/home/mauro/gitrepos/self-home/sql/domo2.db"
LOGS_CONFIG = r"/home/mauro/gitrepos/self-home/resources/logs.json"