
import time

from microscope_control import MicroscopeController


def on_event(event_name, t_delay):
    print(event_name, t_delay)


while True:
    microscope = MicroscopeController()
    microscope.callback_events = on_event

    microscope.wait_until_connected()

    microscope.move_west(1)
    time.sleep(100)
