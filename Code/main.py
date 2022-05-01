import re
import socket
import uuid
from typing import List, Dict
import netifaces
import SocketHandler, ssl_generation
from StartUp.broadcasting import *
from SQLManagment.SQLClient import SQLClient
from GUI.GUIClient import GUIClient


def start_up(my_sockets: MultiSocket,sql_client: SQLClient):
    sql_client.create_tables()
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
    for i in addr:
        if "127" == i["adrr"][0:4]:
            addr.remove(i)
    return l


def main():
    db_client = SQLClient(db_file_name=Constants.DATABASE_FILE_NAME)
    adrr = []
    for i in netifaces.interfaces():
        try:
            adrr.append(netifaces.ifaddresses(i)[netifaces.AF_INET][0])
        except:
            continue

    adrr = sort_adrr(adrr, "addr")
    print(adrr)
    network_config = adrr[1]
    Constants.BROADCAST_IP = network_config["broadcast"]
    my_computer = Computer(ip=network_config["addr"],
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.LISTENING_SERVER_PORT, subnet_mask=network_config["netmask"])
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.SERVER_FILE}.key",
                            CERT_FILE=f"{Constants.SERVER_FILE}.crt")
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.CLIENT_FILE}.key",
                            CERT_FILE=f"{Constants.CLIENT_FILE}.crt")
    my_sockets = MultiSocket(my_computer)
    print(my_computer)

    start_up(my_sockets,db_client)
    gui = GUIClient(db_client,my_sockets)

main()
