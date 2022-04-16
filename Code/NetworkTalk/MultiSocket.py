import socket
from typing import Dict

from Code import globals
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.constants import Constants


class MultiSocket(object):
    _server_sockets: dict[Computer, socket.socket]
    _client_sockets: dict[Computer, socket.socket]
    _receiving_socket: socket.socket

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

    def add_server_sockets(self, connected_computer: Computer) -> None:
        print(connected_computer)
        print(f"CLIENTS {self.client_sockets}")
        print(f"SERVERS {self._server_sockets}")
        if connected_computer not in self._server_sockets:
            self._server_sockets[connected_computer] = socket.socket()
            self._server_sockets[connected_computer].connect((connected_computer.ip, connected_computer.port))
        else:
            try:
                self._server_sockets[connected_computer].send(b"still alive?")
            except:
                del self._server_sockets[connected_computer]
                self._server_sockets[connected_computer] = socket.socket()
                self._server_sockets[connected_computer].connect((connected_computer.ip, connected_computer.port))
        if self.get_computer_from_ip_client_sockets(connected_computer.ip) is not None and self.get_computer_from_ip_client_sockets(connected_computer.ip).name == "":
            client_computer = self.get_computer_from_ip_client_sockets(connected_computer.ip)
            client_computer.mac, client_computer.subnet_mask, client_computer.port, client_computer.name = connected_computer.mac, connected_computer.subnet_mask, connected_computer.port, connected_computer.name

    def get_computer_from_ip_server_sockets(self, ip: str):
        for i in self._server_sockets.keys():
            if ip == i.ip:
                return i
        return None

    def get_computer_from_ip_client_sockets(self, ip: str):
        for i in self._client_sockets.keys():
            if ip == i.ip:
                return i
        return None

    def add_client_sockets(self, computer: Computer, client_socket: socket.socket):

        self._client_sockets[computer] = client_socket
        globals.logger.info(f"{computer} add client_socket {client_socket}")

    def broadcast_message(self, message: str) -> None:
        self._broadcast_send_socket.sendto(message.encode(), (Constants.broadcast_ip, Constants.udp_listening_port))
        globals.logger.info(f"sent broadcast '{message}'")

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
