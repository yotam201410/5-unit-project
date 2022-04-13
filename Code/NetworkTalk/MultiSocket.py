import socket
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.constants import Constants
from typing import Dict
from Code import globals


class MultiSocket(object):
    def __init__(self, computer: Computer):
        self._client_sockets = {}
        self._server_sockets = {}
        self._receiving_socket = socket.socket()
        self._broadcast_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._broadcast_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._udp_server_socket.bind((computer.ip, Constants.udp_listening_port))
        self._receiving_socket.bind((computer.ip, computer.port))
        self._computer = computer

    @property
    def computer(self) -> Computer:
        return self._computer

    def open_socket(self) -> None:
        self._receiving_socket.listen()

    def add_computer(self, computer: Computer, client_socket: socket.socket) -> None:
        self._client_sockets[computer] = client_socket
        self._server_sockets[computer] = socket.socket()
        self._server_sockets[computer].connect((computer.ip, computer.port))

    def broadcast_message(self, message: str) -> None:
        self._broadcast_send_socket.sendto(message.encode(), (Constants.broadcast_ip, Constants.udp_listening_port))
        globals.logger.debug(f"sent broadcast '{message}'")

    @property
    def udp_server_socket(self) -> socket.socket:
        return self._udp_server_socket

    @property
    def receiving_socket(self) -> socket.socket:
        return self._receiving_socket

    @property
    def client_sockets(self) -> Dict[Computer, socket.socket]:
        return self._client_sockets

    @property
    def server_sockets(self) -> Dict[Computer, socket.socket]:
        return self._server_sockets
