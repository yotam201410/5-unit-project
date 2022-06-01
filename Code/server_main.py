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
from WebApp import http_app,https_app

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
def start_gui_connection(ip,port,my_sockets:MultiSocket,host_client: HostClient):
    server_socket = socket.socket()
    server_socket = ssl.wrap_socket(server_socket,keyfile="server.key",server_side=True,certfile="server.crt")
    server_socket.bind((ip,port))
    server_socket.listen()
    print(server_socket)
    while True:
        try:
            connected_socket,__ = server_socket.accept()
            while True:
                try:
                    print(connected_socket)
                    data = connected_socket.recv(1024)
                    decrypted_data = data.decode()
                    print(decrypted_data)
                    if decrypted_data.startswith("sign_up"):
                        splited = decrypted_data.split(" ")
                        username=splited[1]
                        password = splited[2]
                        my_sockets.add_user(username,password)
                    elif decrypted_data.startswith("add_domain"):
                        splited = decrypted_data.split(" ")
                        domain=splited[1]
                        host_client.add_domain(domain)
                        my_sockets.add_domain(domain)
                    elif decrypted_data.startswith("remove_domain"):
                        splited = decrypted_data.split(" ")
                        domain=splited[1]
                        host_client.remove_domain(domain)
                        my_sockets.remove_domain(domain)
                    elif decrypted_data.startswith("delete_user"):
                        splited = decrypted_data.split(" ")
                        username=splited[1]
                        my_sockets.remove_user(username)
                except Exception as e:
                    raise e 
        except Exception as e:
            raise e 




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
    my_computer = Computer(ip=network_config["addr"],
                           mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
                           port=Constants.LISTENING_SERVER_PORT, subnet_mask=network_config["netmask"])
    print(my_computer)
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.SERVER_FILE}.key",
                            CERT_FILE=f"{Constants.SERVER_FILE}.crt")
    ssl_generation.cert_gen(commonName=my_computer.name, KEY_FILE=f"{Constants.CLIENT_FILE}.key",
                            CERT_FILE=f"{Constants.CLIENT_FILE}.crt")
    my_sockets = MultiSocket(my_computer, (network_config["broadcast"], Constants.UDP_LISTENING_PORT))

    start_up(my_sockets, db_client, host_client)
    print("Socket Is Up")
    threading.Thread(target = http_app.main).start()
    threading.Thread(target=https_app.main).start()
    print("http/s servers are up")
    threading.Thread(target=start_gui_connection,args=(my_computer.ip,Constants.server_port,my_sockets,host_client)).start()



if __name__ == '__main__':
    if is_admin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
