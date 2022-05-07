import socket
from typing import Dict
from SQLManagment.SQLClient import SQLClient

import globals
from NetworkTalk.Computer import Computer
from constants import Constants
from typing import *
import ssl


class NoSuchComputer(Exception):
    pass


class MultiSocket(object):
    connected_computers: Dict[str, Computer]
    _receiving_socket: ssl.SSLSocket | socket.socket

    def __init__(self, computer: Computer, broadcast_address: Tuple[str, int]):
        self.broadcast_address = broadcast_address
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
        self._broadcast_send_socket.sendto(message.encode(), self.broadcast_address)
        globals.logger.info(f"sent broadcast '{message}', {self.broadcast_address}")

    @property
    def udp_server_socket(self) -> socket.socket:
        return self._udp_server_socket

    @property
    def receiving_socket(self) -> ssl.SSLSocket:
        return self._receiving_socket

    def sync_data(self, sql_client: SQLClient):
        for connected_computer_ip in self.connected_computers:
            server_socket = self.connected_computers[connected_computer_ip].server_socket
            for user_data in sql_client.get_all_users():
                server_socket.send(f"add user {user_data[0]} {user_data[1]}".encode())
            for domain in sql_client.get_host_rows():
                server_socket.send(f"add domain {domain[0]}".encode())

    def add_user(self, username, password):
        for connected_computer_ip in self.connected_computers:
            server_socket = self.connected_computers[connected_computer_ip].server_socket
            server_socket.send(f"add user {username} {password}".encode())

    def add_domain(self, domain):
        for connected_computer_ip in self.connected_computers:
            server_socket = self.connected_computers[connected_computer_ip].server_socket
            server_socket.send(f"add domain {domain}".encode())

    def remove_domain(self, domain):
        for connected_computer_ip in self.connected_computers:
            server_socket = self.connected_computers[connected_computer_ip].server_socket
            server_socket.send(f"remove domain {domain}".encode())

    def remove_user(self, username):
        for connected_computer_ip in self.connected_computers:
            server_socket = self.connected_computers[connected_computer_ip].server_socket
            server_socket.send(f"remove user {username}".encode())
