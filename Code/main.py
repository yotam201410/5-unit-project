import re
import socket
import threading
import uuid

from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code.StartUp.broadcasting import *
from Code.NetworkTalk.constants import Constants


def start_up(my_sockets:MultiSocket):
    threading.Thread(target=start_broadcast_setup, args=(my_sockets,)).start()


def main():
    my_computer = Computer(ip=socket.gethostbyname(socket.gethostname()),
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.listening_server_port)
    my_sockets = MultiSocket(my_computer)
    start_up(my_sockets)


if __name__ == "__main__":
    main()
