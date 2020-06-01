
import time

from tcp_controls.microscope_control import MicroscopeController


while True:
    microscope = MicroscopeController()

    microscope.wait_until_connected()

    microscope.set_light_intensity(0)
    time.sleep(1)
    microscope.set_light_intensity(1)
    time.sleep(1)
    microscope.set_light_intensity(0.5)
    time.sleep(0.5)
    microscope.set_light_intensity(0.6)
    time.sleep(0.5)
    microscope.set_light_intensity(0.7)
    time.sleep(0.5)
    microscope.set_light_intensity(0.8)
    time.sleep(0.5)
    microscope.set_light_intensity(1)

    microscope.move_north(1)
    microscope.move_east(0.3)
    time.sleep(5)
    microscope.move_south(1)
    time.sleep(5)
    microscope.stop_move()
    microscope.stop_zoom()

    microscope.move_east(0.5)
    time.sleep(5)
    microscope.move_west(0.5)
    time.sleep(5)
    microscope.stop_move()
    microscope.stop_zoom()

    microscope.zoom_in(1)
    time.sleep(5)
    microscope.zoom_out(1)
    time.sleep(5)
    microscope.stop_move()
    microscope.stop_zoom()
