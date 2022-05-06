import re
import socket
import uuid
from typing import List, Dict
import ctypes, sys
import SocketHandler
import netifaces
import ssl_generation
from GUI.GUIClient import GUIClient
from SQLManagment.SQLClient import SQLClient
from StartUp.broadcasting import *
from HostFileManagment.HostManagment import HostClient


def start_up(my_sockets: MultiSocket, sql_client: SQLClient, host_client: HostClient):
    sql_client.create_tables()
    threading.Thread(target=start_broadcast_setup, args=(my_sockets, sql_client, host_client)).start()
    threading.Thread(target=SocketHandler.handle_connections_wrapper,
                     args=(my_sockets, sql_client, host_client)).start()


def get_min(addr: List[Dict[str, str]], by: str):
    min_index = 0
    for i in range(len(addr)):
        minimum = addr[i][by]
        min_index = i
        for j in range(len(addr)):
            current_split = [int(y) for y in addr[j][by].split('.')]
            splitted_min = [int(x) for x in minimum.split('.')]
            if splitted_min[0] == current_split[0]:
                if splitted_min[1] == current_split[1]:
                    if splitted_min[2] == current_split[2]:
                        if splitted_min[3] > current_split[3]:
                            minimum = addr[j][by]
                            min_index = j
                    elif splitted_min[2] > current_split[2]:
                        minimum = addr[j][by]
                        min_index = j

                elif splitted_min[1] > current_split[1]:
                    minimum = addr[j][by]
                    min_index = j

            elif splitted_min[0] > current_split[0]:
                minimum = addr[j][by]
                min_index = j
    return min_index


def sort_addr(addr: List[Dict[str, str]], by: str):
    returned_list = []
    for i in range(len(addr)):
        index = get_min(addr, by)
        returned_list.append(addr[index])
        addr.remove(addr[index])
    return returned_list


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    host_client = HostClient()
    db_client = SQLClient(db_file_name=Constants.DATABASE_FILE_NAME)
    print("DB is UP")
    addr = []
    for i in netifaces.interfaces():
        try:
            addr.append(netifaces.ifaddresses(i)[netifaces.AF_INET][0])
        except:
            continue

    addr = sort_addr(addr, "addr")
    network_config = addr[1]
    Constants.BROADCAST_IP = network_config["broadcast"]
    my_computer = Computer(ip=network_config["addr"],
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.LISTENING_SERVER_PORT, subnet_mask=network_config["netmask"])
    print(my_computer)
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.SERVER_FILE}.key",
                            CERT_FILE=f"{Constants.SERVER_FILE}.crt")
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.CLIENT_FILE}.key",
                            CERT_FILE=f"{Constants.CLIENT_FILE}.crt")
    my_sockets = MultiSocket(my_computer)

    start_up(my_sockets, db_client, host_client)
    print("Socket Is Up")
    gui = GUIClient(db_client, my_sockets, host_client=host_client)


if is_admin():
    main()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
