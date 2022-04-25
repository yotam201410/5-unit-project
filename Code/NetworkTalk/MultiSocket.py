import socket
from typing import Dict

from Code import globals
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.constants import Constants
from typing import *
import ssl


class NoSuchComputer(Exception):
    pass


class MultiSocket(object):
    connected_computers: Dict[str, Computer]
    _receiving_socket: ssl.SSLSocket | socket.socket

    def __init__(self, computer: Computer):
        self.connected_computers = {}
        self._receiving_socket = socket.socket()
        self._broadcast_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._broadcast_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._udp_server_socket.bind((computer.ip, Constants.UDP_LISTENING_PORT))
        self._receiving_socket.bind((computer.ip, computer.port))
        self._receiving_socket = ssl.wrap_socket(self._receiving_socket, cert_reqs=ssl.CERT_NONE, server_side=True,
                                                 keyfile=f"{Constants.SERVER_FILE}.key",
                                                 certfile=f"{Constants.SERVER_FILE}.crt")
        self._computer = computer

    @property
    def computer(self) -> Computer:
        return self._computer

    def open_socket(self) -> None:
        self._receiving_socket.listen()

    def broadcast_message(self, message: str) -> None:
        self._broadcast_send_socket.sendto(message.encode(), (Constants.BROADCAST_IP, Constants.UDP_LISTENING_PORT))
        globals.logger.info(f"sent broadcast '{message}'")

    @property
    def udp_server_socket(self) -> socket.socket:
        return self._udp_server_socket

    @property
    def receiving_socket(self) -> ssl.SSLSocket:
        return self._receiving_socket
