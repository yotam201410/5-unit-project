import logging
from ssl import SSLSocket
from NetworkTalk.Computer import Computer
from NetworkTalk.MultiSocket import MultiSocket
from typing import Tuple
import threading
import globals


def handle_connections(my_sockets: MultiSocket, client_socket: SSLSocket, client_address: Tuple[str, int]):
    if client_address[0] not in my_sockets.connected_computers:
        my_sockets.connected_computers[client_address[0]] = Computer(ip=client_address[0], client_socket=client_socket)
        connected_computer = my_sockets.connected_computers[client_address[0]]
    else:
        connected_computer = my_sockets.connected_computers[client_address[0]]
        connected_computer.client_socket = client_socket
    while True:
        recived_data = client_socket.recv(1024)
        if recived_data != b'':
            logging.info(f"got {recived_data} from {connected_computer}")


def handle_connections_wrapper(my_sockets: MultiSocket):
    my_sockets.receiving_socket.listen()
    while True:
        client_socket, tcp_address = my_sockets.receiving_socket.accept()
        globals.logger.info(f"new client connected from {tcp_address}")
        threading.Thread(target=handle_connections, args=(my_sockets, client_socket, tcp_address)).start()
