import time
import threading

DEFAULT_TIMEOUT = 10

events = {}
waiting_event = {}


def on(event, callback):
    global events
    if event not in events:
        events[event] = []
    events[event].append(callback)


def emit(event_name, msg):
    global events, waiting_event
    if event_name in events:
        for event in events[event_name]:
            event(msg)
    if event_name in waiting_event:
        waiting_event[event_name].set()


def wait_for(event_name, timeout=None):
    global waiting_event
    waiting_event[event_name] = threading.Event()
    if timeout is None:
        waiting_event[event_name].wait()
    else:
        waiting_event[event_name].wait(timeout)
    del waiting_event[event_name]


def wait_for_first(event_name_list, timeout=DEFAULT_TIMEOUT):
    global waiting_event
    for event_name in event_name_list:
        waiting_event[event_name] = threading.Event()
    while True:
        for event_name in event_name_list:
            if waiting_event[event_name].wait(timeout):
                return
