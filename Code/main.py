import re
import socket
import uuid
from typing import List, Dict

import netifaces
from Code import SocketHandler, ssl_generation
from Code.StartUp.broadcasting import *


def start_up(my_sockets: MultiSocket):
    threading.Thread(target=start_broadcast_setup, args=(my_sockets,)).start()
    threading.Thread(target=SocketHandler.handle_connections_wrapper, args=(my_sockets,)).start()


def get_min(addr: List[Dict[str, str]], by: str):
    min_index = 0
    for i in range(len(addr)):
        min = addr[i][by]
        min_index = i
        for j in range(len(addr)):
            current_split = [int(y) for y in addr[j][by].split('.')]
            splited_min = [int(x) for x in min.split('.')]
            if splited_min[0] == current_split[0]:
                if splited_min[1] == current_split[1]:
                    if splited_min[2] == current_split[2]:
                        if splited_min[3] > current_split[3]:
                            min = addr[j][by]
                            min_value = addr[j]
                            min_index = j
                    elif splited_min[2] > current_split[2]:
                        min = addr[j][by]
                        min_value = addr[j]
                        min_index = j

                elif splited_min[1] > current_split[1]:
                    min = addr[j][by]
                    min_value = addr[j]
                    min_index = j

            elif splited_min[0] > current_split[0]:
                min = addr[j][by]
                min_value = addr[j]
                min_index = j
    return min_index


def sort_adrr(addr: List[Dict[str, str]], by: str):
    l = []
    for i in range(len(addr)):
        index = get_min(addr, by)
        l.append(addr[index])
        addr.remove(addr[index])

    return l


def main():
    adrr = []
    for i in netifaces.interfaces():
        try:
            adrr.append(netifaces.ifaddresses(i)[netifaces.AF_INET][0])
        except:
            continue
    print(adrr)

    adrr = sort_adrr(adrr, "addr")
    print(adrr)
    network_config = adrr[1]
    Constants.broadcast_ip = network_config["broadcast"]
    my_computer = Computer(ip=network_config["addr"],
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.listening_server_port, subnet_mask=network_config["netmask"])
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.server_file}.key",
                            CERT_FILE=f"{Constants.server_file}.crt")
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.client_file}.key",
                            CERT_FILE=f"{Constants.client_file}.crt")
    my_sockets = MultiSocket(my_computer)
    print(my_computer)


    start_up(my_sockets)


main()
