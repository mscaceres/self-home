#{topic:[(callback,message_filter)]}
db = {}


def _index_of(seq, listener):
    for i, t in enumerate(seq):
        if t[0] == listener:
            return i
    return None

ALL = "EVENT_DISPACHER_ALL_TOPICS"


def subscribe(topic, listener, message_filter=None):
    if topic in db:
        db[topic].append((listener, message_filter))
    else:
        db[topic] = [(listener, message_filter)]


def unsubscribe(topic, listener):
    if topic in db:
        i = _index_of(db[topic], listener)
        db[topic].pop(i)
        if not db[topic]:
            unsubscribe_all(topic)


def unsubscribe_all(topic=None):
    if topic is None:
        db.clear()
    else:
        del db[topic]


def is_subscribed(topic, listener):
    return (topic in db and _index_of(db[topic], listener) is not None)


def send_message(topic, message):
    if topic in db:
        for listener, message_filter in db[topic]:
            _call_listener(topic, message, listener, message_filter)
        if ALL in db.keys():
            for listener, message_filter in db[ALL]:
                _call_listener(topic, message, listener, message_filter)


def _filter_message(message_filter, message):
    msg = None
    if message_filter is None or message_filter(message):
        msg = message
    return msg


def _call_listener(topic, message, listener, message_filter):
    msg = _filter_message(message_filter, message)
    if msg is not None:
        listener(topic, message)
