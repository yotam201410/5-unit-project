from socket import socket
import logging

log = logging.getLogger()


class Computer(object):
    def __init__(self, ip: str, mac: str, name: str, port: int):
        assert type(ip) == str
        assert type(mac) == str
        assert type(name) == str
        assert type(port) == int

        self._ip = ip
        self._mac = mac
        self._name = name
        self._port = port

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

    @mac.setter
    def mac(self, mac: str):
        assert type(mac) == str
        self._mac = mac

    @ip.setter
    def ip(self, ip: str):
        assert type(ip) == str
        self._ip = ip

    @name.setter
    def name(self, name: str):
        assert type(name) == str

    def __str__(self) -> str:
        return f"{self.name} , {self.ip}, {self.port}, {self.mac}"

    def __hash__(self) -> int:
        return hash((self.name, self.ip, self.port, self.mac))

    def __eq__(self, other) -> bool:
        assert type(other) == Computer
        return self.__hash__() == hash(other)

    def __dict__(self) -> dict:
        return {"name": self.name, "port": self.port, "mac": self.mac, "ip": self.ip}
