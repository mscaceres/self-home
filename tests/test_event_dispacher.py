import pytest


@pytest.fixture
def ed():
    import domo.event_dispacher as ed
    ed.DB = {}
    return ed


def test_subscribe_single_topic(ed):
    ed.subscribe("T1", lambda x: x, lambda x: True)
    ed.subscribe("T1", lambda x: x, lambda x: True)
    assert (len(ed.DB.keys()) == 1 and len(ed.DB['T1']) == 2)


def test_subscribe_multiple_topics(ed):
    for i in range(100):
        ed.subscribe(str(i), lambda x: x, lambda x: True)
    assert (len(ed.DB.keys()) == 100 and len(ed.DB.values()) == 100)


def test_unsubscribe_empty_listeners(ed):
    listener = lambda x: x
    ed.subscribe("T1", listener, lambda x: True)
    ed.unsubscribe("T1", listener)
    assert "T1" not in ed.DB


def test_unsubscribe_remaining_listeners(ed):
    listener = lambda x: x
    listener2 = lambda y: y
    ed.subscribe("T1", listener, lambda x: True)
    ed.subscribe("T1", listener2, lambda x: True)
    ed.unsubscribe("T1", listener)
    assert (len(ed.DB["T1"]) == 1)


def test_unsubscribe_all_with_Topic(ed):
    listener = lambda x: x
    listener2 = lambda y: y
    ed.subscribe("T1", listener, lambda x: True)
    ed.subscribe("T2", listener2, lambda x: True)
    ed.unsubscribe_all("T1")
    assert ("T1" not in ed.DB and len(ed.DB["T2"]) == 1)


def test_unsubscribe_all_without_topic(ed):
    listener = lambda x: x
    listener2 = lambda y: y
    ed.subscribe("T1", listener, lambda x: True)
    ed.subscribe("T2", listener2, lambda x: True)
    ed.unsubscribe_all()
    assert not ed.DB


def test_is_subscribed_not_topic(ed):
    assert False is ed.is_subscribed("T1", lambda x: x)


def test_is_subscribed_exist(ed):
    listener = lambda x: x
    ed.subscribe("T1", listener, lambda x: True)
    assert True is ed.is_subscribed("T1", listener)


def test_is_subscribed_not_listener(ed):
    listener = lambda x: x
    ed.subscribe("T1", listener, lambda x: True)
    assert False is ed.is_subscribed("T1", lambda y: y)


# def test_filter_message_match(ed):
#     f = lambda x: x == "hola"
#     msg = ed._filter_message(f, "hola")
#     assert msg == "hola"
#
#
# def test_filter_message_not_match(ed):
#     f = lambda x: x == "hola1"
#     msg = ed._filter_message(f, "hola")
#     assert msg is None
#
#
# def test_empty_filter(ed):
#     msg = ed._filter_message(None, "hola")
#     assert msg is "hola"


def test_send_message(ed):
    msg = []
    listener = lambda t, msg: msg.append(1)
    listener2 = lambda t, msg: msg.append(2)
    ed.subscribe("T1", listener, lambda x: True)
    ed.subscribe("T1", listener2, lambda x: True)
    ed.send_message("T1", msg)
    assert (1 in msg and 2 in msg)


def test_send_message_some_filtered(ed):
    msg = []
    listener = lambda t, msg: msg.append(1)
    listener2 = lambda t, msg: msg.append(2)
    ed.subscribe("T1", listener, lambda x: True)
    ed.subscribe("T1", listener2, lambda x: False)
    ed.send_message("T1", msg)
    assert (1 in msg and 2 not in msg)


def test_send_message_ALL_topic(ed):
    msg = []
    listener = lambda t, msg: msg.append(1)
    listener2 = lambda t, msg: msg.append(2)
    ed.subscribe(ed.ALL, listener, lambda x: True)
    ed.subscribe("T1", listener2, lambda x: True)
    ed.send_message("T1", msg)
    assert (1 in msg and 2 in msg)
