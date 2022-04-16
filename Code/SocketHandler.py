import logging
import socket
from Code.NetworkTalk.MultiSocket import MultiSocket
from typing import Tuple
import threading
from Code import globals


def handle_connections(my_sockets: MultiSocket, client_socket: socket.socket, client_address: Tuple[str, int]):
    connected_computer = my_sockets.get_computer_from_ip_client_sockets(client_address[0])
    my_sockets.client_sockets[connected_computer] = client_socket
    if connected_computer is None:
        print()
        raise Exception("idk wtf juts happened")
    while True:
        recived_data = client_socket.recv(1024)
        logging.info(f"got {recived_data} from {connected_computer}")


def handle_connections_wrapper(my_sockets: MultiSocket):
    my_sockets.receiving_socket.listen()
    while True:
        client_socket, tcp_address = my_sockets.receiving_socket.accept()
        globals.logger.info(f"new client connected from {tcp_address}")
        threading.Thread(target=handle_connections, args=(my_sockets, client_socket, tcp_address)).start()
