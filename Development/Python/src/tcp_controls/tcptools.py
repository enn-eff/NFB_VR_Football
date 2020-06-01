
import socket
import json
import sys


def get_error_set(str_errortype):
    if str_errortype == 'ConnectionError':
        # Proceed depending on Python version
        if sys.version_info[0] < 3:
            error_set = (socket.error,)
        else:
            error_set = (ConnectionAbortedError, ConnectionResetError,)
    elif str_errortype == 'ConnectionTimeout':
        error_set = (socket.timeout,)
    else:
        raise ValueError(str_errortype)

    return error_set


def get_socket_at_free_port():
    # Parameters for socket
    # Note: port = 0 for making OS pick a free number between 1024 and 65535
    # address_server = ('localhost', 8001)
    address_server = ('localhost', 0)

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind at specified port (0 for automatic port selection) and then get port number
    s.bind(address_server)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = s.getsockname()[1]

    address_server = ('localhost', port)

    return s, address_server


def get_n_bytes_send_max(n_bytes_config):
    # n_bytes_send_max = np.power(256, n_bytes_config) => results in 0 ??
    n_bytes_send_max = 256
    for i in range(n_bytes_config-1):
        n_bytes_send_max = n_bytes_send_max * 256

    return n_bytes_send_max


def send_dict_as_json(dict_msg, conn, n_bytes_config=4, encoding='utf-8'):
    # Maximum number of bytes for the message in json format
    n_bytes_send_max = get_n_bytes_send_max(n_bytes_config)

    # Convert message dict to string of json format
    json_msg = json.dumps(dict_msg)

    # Convert message string to byte representation
    bytes_msg = json_msg.encode(encoding)

    # Check length of byte array
    n_bytes_send = len(bytes_msg)
    if n_bytes_send > n_bytes_send_max:
        raise RuntimeError('Message to long: ' + str(n_bytes_send) + ' (max. ' + str(n_bytes_send_max) + ')')

    # Convert length of byte array (int) to byte representation (big-endian)
    bytes_config = convert_int_to_bytes(n_bytes_send, n_bytes_config)

    #print('Sending', n_bytes_send, 'bytes => config bytes:', bytes_config)

    # Send
    conn.sendall(bytes_config)
    conn.sendall(bytes_msg)

    # Wait for response
    response = conn.recv(1)
    # print('Received', response)


def receive_next_message(conn, n_bytes_config=4, encoding='utf-8'):
    # Step 1: Read the "config bytes" (specify the length of the actual message)
    response = conn.recv(n_bytes_config)
    n_bytes_msg = int.from_bytes(response, byteorder='big')
    # print(response, n_bytes_msg)

    # Step 2: Read the actual message
    response = conn.recv(n_bytes_msg)
    # str_msg = response.decode(encoding)
    # print(response)
    dict_msg = json.loads(response)

    # Step 3: Respond by sending some byte
    confirmation_byte = b'\x01'
    conn.sendall(confirmation_byte)

    return dict_msg


def convert_int_to_bytes(n_bytes_send, n_bytes_config):
    # Proceed depending on Python version
    if sys.version_info[0] < 3:
        bytes_config = to_bytes(n_bytes_send, n_bytes_config, 'big')
    else:
        bytes_config = n_bytes_send.to_bytes(n_bytes_config, 'big')

    return bytes_config


def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]
