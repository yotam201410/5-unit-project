from __future__ import annotations

from socket import socket
import logging
from typing import Optional
import ssl
log = logging.getLogger()


class Computer(object):
    def __init__(self, ip: str = "0.0.0.0", subnet_mask: str = "0.0.0.0", mac: str = "0.0.0.0.0.0", name: str = "",
                 port: int = -1, server_socket: Optional[ssl.SSLSocket] = None, client_socket: Optional[ssl.SSLSocket] = None):
        assert type(ip) == str
        assert type(mac) == str
        assert type(name) == str
        assert type(port) == int
        assert type(subnet_mask) == str
        self._ip = ip
        self._mac = mac
        self._name = name
        self._port = port
        self._subnet_mask = subnet_mask
        self.server_socket = server_socket
        self.client_socket = client_socket

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def name(self) -> str:
        return self._name

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int):
        assert type(port) == int
        self._port = port

    @ip.setter
    def ip(self, ip: str):
        assert type(ip) == str
        self._ip = ip

    @name.setter
    def name(self, name: str):
        assert type(name) == str
        self._name = name

    def __str__(self) -> str:
        return f"{self.name}, {self.ip}, {self.subnet_mask}, {self.port}, {self.mac}"

    def __hash__(self) -> int:
        return hash((self.name, self.subnet_mask, self.ip, self.port, self.mac))

    def __eq__(self, other) -> bool:
        assert type(other) == Computer
        return self.__hash__() == hash(other)

    def __dict__(self) -> dict:
        return {"name": self._name, "port": self._port, "mac": self._mac, "ip": self._ip,
                "subnet mask": self._subnet_mask, "server_socket": self.server_socket,
                "client_socket": self.client_socket}

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__())

    @property
    def subnet_mask(self) -> str:
        return self._subnet_mask

    @subnet_mask.setter
    def subnet_mask(self, subnet: str) -> None:
        assert type(subnet) == str
        self._subnet_mask = subnet

    @mac.setter
    def mac(self, mac: str) -> None:
        assert type(mac) == str
        self._mac = mac

    def update_computer(self, computer: Computer):
        self._ip = computer.ip
        self._mac = computer.mac
        self._port = computer.port
        self._subnet_mask = computer.subnet_mask
        self._name = computer._name
