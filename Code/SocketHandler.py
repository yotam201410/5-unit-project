import socket
from Code.NetworkTalk.MultiSocket import MultiSocket
from typing import Tuple
import threading
from Code import globals


def handle_connections(my_sockets: MultiSocket, client_socket: socket.socket, client_address: Tuple[str, int]):
    computer = my_sockets.get_computer_from_ip(client_address[0])
    if computer not in my_sockets.client_sockets or my_sockets.client_sockets[computer] is None:
        my_sockets.add_client_sockets(computer=computer, client_socket=client_socket)

    else:
        while True:
            recived_data = my_sockets.server_sockets[computer].recv(1024)
            if recived_data.decode() == "still alive?":
                pass


def handle_connections_wrapper(my_sockets: MultiSocket):
    my_sockets.receiving_socket.listen()
    while True:
        client_socket, tcp_address = my_sockets.receiving_socket.accept()
        globals.logger.info(f"new client connected from {tcp_address}")
        threading.Thread(target=handle_connections, args=(my_sockets, client_socket, tcp_address)).start()
