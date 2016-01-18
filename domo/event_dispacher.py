#{topic:[(callback,message_filter)]}
DB = {}


def _index_of(seq, listener):
    for i, t in enumerate(seq):
        if t[0] == listener:
            return i
    return None

ALL = "EVENT_DISPACHER_ALL_TOPICS"


def subscribe(topic, listener, message_filter=None):
    if topic in DB:
        DB[topic].append((listener, message_filter))
    else:
        DB[topic] = [(listener, message_filter)]


def unsubscribe(topic, listener):
    if topic in DB:
        i = _index_of(DB[topic], listener)
        DB[topic].pop(i)
        if not DB[topic]:
            unsubscribe_all(topic)


def unsubscribe_all(topic=None):
    if topic is None:
        DB.clear()
    else:
        del DB[topic]


def is_subscribed(topic, listener):
    return (topic in DB and _index_of(DB[topic], listener) is not None)


# def send_message(topic, message):
#     if topic in DB:
#         for listener, message_filter in DB[topic]:
#             _call_listener(topic, message, listener, message_filter)
#         if ALL in DB:
#             for listener, message_filter in DB[ALL]:
#                 _call_listener(topic, message, listener, message_filter)


def send_message(topic, message):
    topics = [topic]
    if ALL in DB:
        topics.append(ALL)
    for listener, topic in _filtered_listeners(topics, message):
        listener(topic, message)


def _filtered_listeners(topics, message):
    for topic in topics:
        try:
            for listener, message_filter in DB[topic]:
                if message_filter is None or message_filter(message):
                    yield listener, topic
        except KeyError:
            continue


def _filter_message(message_filter, message):
    msg = None
    if message_filter is None or message_filter(message):
        msg = message
    return msg


def _call_listener(topic, message, listener, message_filter):
    msg = _filter_message(message_filter, message)
    if msg is not None:
        listener(topic, message)
