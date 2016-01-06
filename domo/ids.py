# -*- coding: utf-8 -*-
import uuid

def get_id(id=None):
    uid = None
    if id is None:
        uid = uuid.uuid1()
    elif type(id) is int:
        uid = uuid.UUID(int=id)
    elif type(id) is str:
        uid = uuid.UUID(id)
    else:
        raise ValueError("{} is not integer or string".format(id))
    return uid
