import logging
from ssl import SSLSocket
from NetworkTalk.Computer import Computer
from NetworkTalk.MultiSocket import MultiSocket
from typing import Tuple
import threading
import globals
from SQLManagment.SQLClient import SQLClient
from HostFileManagment.HostManagment import HostClient
import sqlite3


def handle_connections(my_sockets: MultiSocket, client_socket: SSLSocket, client_address: Tuple[str, int],
                       sql_client: SQLClient, host_client: HostClient):
    if client_address[0] not in my_sockets.connected_computers:
        my_sockets.connected_computers[client_address[0]] = Computer(ip=client_address[0], client_socket=client_socket)
        connected_computer = my_sockets.connected_computers[client_address[0]]
    else:
        connected_computer = my_sockets.connected_computers[client_address[0]]
        connected_computer.client_socket = client_socket
    while True:
        recived_data = client_socket.recv(1024)
        if recived_data != b'':
            decoded_data = recived_data.decode()
            logging.info(f"got {decoded_data} from {connected_computer}")
            if decoded_data.startswith("add domain"):
                splited_decoded_data = decoded_data.split(" ")
                sql_client.add_data_to_table("host", ("domain",), (splited_decoded_data[2],))
                host_client.add_domain(splited_decoded_data[2])
            elif decoded_data.startswith("remove domain"):
                splited_decoded_data = decoded_data.split(" ")
                sql_client.delete_data_from_table("host", where="where domain=?", data=(splited_decoded_data[2],))
                host_client.remove_domain(splited_decoded_data[2])
            elif decoded_data.startswith("add user"):
                try:
                    splited_decoded_data = decoded_data.split(" ")
                    sql_client.add_user(splited_decoded_data[2], splited_decoded_data[3],hashed=False)
                except sqlite3.IntegrityError:
                    pass
                except  Exception as e:
                    raise e
            elif decoded_data.startswith("remove user"):
                try:
                    splited_decoded_data = decoded_data.split(" ")
                    sql_client.delete_user(splited_decoded_data[2])
                except sqlite3.IntegrityError:
                    pass
                except Exception as e:
                    raise e


def handle_connections_wrapper(my_sockets: MultiSocket, sql_client: SQLClient, host_client: HostClient):
    my_sockets.receiving_socket.listen()
    print("server started listening listening")
    while True:
        client_socket, tcp_address = my_sockets.receiving_socket.accept()
        globals.logger.info(f"new client connected from {tcp_address}")
        threading.Thread(target=handle_connections,
                         args=(my_sockets, client_socket, tcp_address, sql_client, host_client)).start()



