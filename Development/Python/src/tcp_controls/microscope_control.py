
import threading
import json
import time
import os
import numpy as np

from src.Microscope_Controller.tcp_controls import tcptools
from src.Microscope_Controller.tcp_controls import tmpfiles


# Initialize set of connection errors that might occur (depends on Python version)
error_sets = dict(
    ConnectionError=tcptools.get_error_set('ConnectionError'),
    ConnectionTimeout=tcptools.get_error_set('ConnectionTimeout'),
)


class MicroscopeController:
    def __init__(self):
        # Encoding
        # encoding = 'ascii'
        self.encoding = 'utf-8'

        self.callback_events = None

        # Constant
        # If changing this, also change nBytesConfig in the receiver!
        self.n_bytes_config = 4

        # Maximum number of bytes for the message in JSON format
        n_bytes_send_max = tcptools.get_n_bytes_send_max(self.n_bytes_config)
        print('Max. number of bytes per message:', n_bytes_send_max)

        self.path_tmp_file = 'user_dir'
        self.filename_tmp_file = 'connection_base_address'

        self.key_cam_vertical = 'planary_move_y'
        self.key_cam_horizontal = 'planary_move_x'
        # self.key_zoom = 'planary_move_z'
        self.key_zoom = 'zoom'
        self.key_light = 'light'

        self.is_running = False

        self.cond_is_connected = threading.Condition()
        self.cond_servers_closed = threading.Condition()

        self.dict_msg = dict()
        self.lock_msg = threading.Lock()

        self.event_msg_in_outbox = threading.Event()
        self.event_server1_connected = threading.Event()
        self.event_server2_connected = threading.Event()
        self.event_server1_closed = threading.Event()
        self.event_server2_closed = threading.Event()
        self.th_connection_handler = threading.Thread(target=self._handle_connection)

        self._start_server()

    def wait_until_connected(self):
        with self.cond_is_connected:
            self.cond_is_connected.wait()

    def stop_zoom(self):
        self._insert_message_content(self.key_zoom, 0)

    def stop_move(self, vertical=True, horizontal=True):
        keys = []
        values = []

        if vertical:
            keys.append(self.key_cam_vertical)
            values.append(0)

        if horizontal:
            keys.append(self.key_cam_horizontal)
            values.append(0)

        self._insert_multiple_message_contents(keys, values)

    def move_north(self, ratio_v):
        """ Moving to the top of camera view """
        sign = + 1
        self._insert_message_content(self.key_cam_vertical, sign*ratio_v)

    def move_south(self, ratio_v):
        """ Moving to the bottom of camera view """
        sign = - 1
        self._insert_message_content(self.key_cam_vertical, sign*ratio_v)

    def move_east(self, ratio_v):
        """ Moving to the right of camera view """
        sign = + 1
        self._insert_message_content(self.key_cam_horizontal, sign*ratio_v)

    def move_west(self, ratio_v):
        """ Moving to the left of camera view """
        sign = - 1
        self._insert_message_content(self.key_cam_horizontal, sign*ratio_v)

    def zoom_in(self, ratio_v):
        """ Zooming in """
        sign = + 1
        self._insert_message_content(self.key_zoom, sign*ratio_v)

    def zoom_out(self, ratio_v):
        """ Zooming out """
        sign = - 1
        self._insert_message_content(self.key_zoom, sign*ratio_v)

    def set_light_intensity(self, ratio_intensity):
        """ Set microscope spotlight intensity (0 ... 1) """
        self._insert_message_content(self.key_light, ratio_intensity)

    def _insert_message_content(self, key, value):
        keys = [key]
        values = [value]
        self._insert_multiple_message_contents(keys, values)

    def _insert_multiple_message_contents(self, keys, values):
        # Insert message
        with self.lock_msg:
            for key, value in zip(keys, values):
                self.dict_msg[key] = value

        # Notify that message is to be send
        self.event_msg_in_outbox.set()

    def _start_server(self):
        self.th_connection_handler.start()

    def _handle_connection(self):
        # Write port number into environment variable
        # Only child processes will be able to access it...
        # os.environ["AVATAR_BASE_PORT"] = str(port)
        # Thus: Create temporary file and save port number there.
        with tmpfiles.TemporaryFile(filename=self.filename_tmp_file, path=self.path_tmp_file) as f:
            self.is_running = True
            while self.is_running:
                self._provide_server_socket(f)

                with self.cond_servers_closed:
                    self.cond_servers_closed.wait()

                self.event_server1_closed.clear()
                self.event_server2_closed.clear()

    def _provide_server_socket(self, f):
        s1, address_server1 = tcptools.get_socket_at_free_port()
        s2, address_server2 = tcptools.get_socket_at_free_port()
        n_connect_accepted = 5

        f.write(
            address_server1[0] + '\n' +
            str(address_server1[1]) + '\n' +
            address_server2[0] + '\n' +
            str(address_server2[1])
        )

        th_server1 = threading.Thread(target=self._run_server_1, args=(s1, address_server1, n_connect_accepted,))
        th_server2 = threading.Thread(target=self._run_server_2, args=(s2, address_server2, n_connect_accepted,))

        th_server1.start()
        th_server2.start()

    def _run_server_1(self, s, address_server, n_connect_accepted):
        s.listen(n_connect_accepted)
        print('[Server] Reset @ ' + str(address_server) + ', waiting for connection...')

        # Catch connection timeouts
        try:
            (conn, address_client) = s.accept()

            self.event_server1_connected.set()
            self._notify_servers_connected()
            print('[Server] Client @ ' + str(address_client) + ' is now connected')

            # Catch other connection errors (e.g. client disconnected)
            try:
                # Run until quit or connection error
                while self.is_running:
                    if self.event_msg_in_outbox.is_set():
                        self._send_outbox_via(conn)

            except error_sets['ConnectionError'] as e:
                print(e)
        except error_sets['ConnectionTimeout'] as e:
            print(e)

        print('Resetting server...')

        conn.close()
        self.event_server1_connected.clear()

        s.close()

        self.event_server1_closed.set()
        self._notify_servers_closed()

    def _run_server_2(self, s, address_server, n_connect_accepted):
        s.listen(n_connect_accepted)
        print('[Server] Reset @ ' + str(address_server) + ', waiting for connection...')

        # Catch connection timeouts
        try:
            (conn, address_client) = s.accept()

            self.event_server2_connected.set()
            self._notify_servers_connected()
            print('[Server] Client @ ' + str(address_client) + ' is now connected')

            # Catch other connection errors (e.g. client disconnected)
            try:
                # Run until quit or connection error
                while self.is_running:
                    self._check_inbox_via(conn)

            except error_sets['ConnectionError'] as e:
                print(e)
        except error_sets['ConnectionTimeout'] as e:
            print(e)

        print('Resetting server...')

        conn.close()
        self.event_server2_connected.clear()

        s.close()

        self.event_server2_closed.set()
        self._notify_servers_closed()

    def _notify_servers_connected(self):
        if self.event_server1_connected.is_set() and self.event_server2_connected.is_set():
            with self.cond_is_connected:
                self.cond_is_connected.notify()

    def _notify_servers_closed(self):
        if self.event_server1_closed.is_set() and self.event_server2_closed.is_set():
            with self.cond_servers_closed:
                self.cond_servers_closed.notify()

    def _send_outbox_via(self, conn):
        with self.lock_msg:
            tcptools.send_dict_as_json(self.dict_msg, conn, self.n_bytes_config, self.encoding)
            self.dict_msg = dict()
        self.event_msg_in_outbox.clear()

    def _check_inbox_via(self, conn):
        msg = tcptools.receive_next_message(conn, self.n_bytes_config, self.encoding)

        if self.callback_events is not None:
            self.callback_events(msg['content']['event_name'], msg['t_delay'])
