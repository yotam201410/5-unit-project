import re
import socket
import threading
import uuid

import netifaces

from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code.StartUp.broadcasting import *
from Code.NetworkTalk.constants import Constants


def start_up(my_sockets:MultiSocket):
    threading.Thread(target=start_broadcast_setup, args=(my_sockets,)).start()


def main():
    adrr = []
    for i in netifaces.interfaces():
        try:
            adrr.append(netifaces.ifaddresses(i)[netifaces.AF_INET][0])
        except:
            continue
    network_config = [x for x in adrr if x["addr"]==socket.gethostbyname(socket.gethostname())][0]
    Constants.broadcast_ip = network_config["broadcast"]
    my_computer = Computer(ip=socket.gethostbyname(socket.gethostname()),
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.listening_server_port,subnet_mask=network_config["netmask"])
    my_sockets = MultiSocket(my_computer)
    print(my_computer)
    start_up(my_sockets)


main()
