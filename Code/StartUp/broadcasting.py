from decimal import DecimalTuple
import time
import threading
from NetworkTalk.Computer import Computer
from NetworkTalk.MultiSocket import MultiSocket
import globals
from constants import Constants
import socket
import ssl
from SQLManagment.SQLClient import SQLClient
from HostFileManagment.HostManagment import HostClient


def handle_client_addition(connected_computer: Computer):
    if connected_computer.server_socket is None:
        connected_computer.server_socket = socket.socket()
        connected_computer.server_socket = ssl.wrap_socket(connected_computer.server_socket, cert_reqs=ssl.CERT_NONE,
                                                           server_side=False,
                                                           keyfile=f"{Constants.CLIENT_FILE}.key",
                                                           certfile=f"{Constants.CLIENT_FILE}.crt")
        connected_computer.server_socket.connect((connected_computer.ip, connected_computer.port))
    else:
        try:
            connected_computer.server_socket.send(b'stiil up?')
        except:
            connected_computer.server_socket = None


def handle_broadcast_answer(my_sockets: MultiSocket, sql_client: SQLClient, host_client: HostClient):
    while True:
        data, udp_addrees = my_sockets.udp_server_socket.recvfrom(1024)
        if udp_addrees[0] != my_sockets.computer.ip:
            decoded_data = data.decode()
            globals.logger.info(f"RECIVED BROADCAST MESSAGE {decoded_data} from {udp_addrees}")
            splited_data = decoded_data.split(',')
            if splited_data[-1] == "up":
                connected_computer = Computer(ip=splited_data[0], subnet_mask=splited_data[1], mac=splited_data[2],
                                              port=int(splited_data[3]), name=splited_data[4])
                if connected_computer.ip in my_sockets.connected_computers:
                    my_sockets.connected_computers[splited_data[0]].update_computer(connected_computer)
                    threading.Thread(target=handle_client_addition,
                                     args=(my_sockets.connected_computers[splited_data[0]],)).start()
                else:
                    my_sockets.connected_computers[splited_data[0]] = connected_computer
                    threading.Thread(target=handle_client_addition,
                                     args=(my_sockets.connected_computers[splited_data[0]],)).start()

            elif splited_data[-1] == "who is up":
                if udp_addrees[0] not in my_sockets.connected_computers:
                    my_sockets.connected_computers[udp_addrees[0]] = Computer(ip=udp_addrees[0])
                my_sockets.broadcast_message(
                    f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")


def broadcast(my_sockets: MultiSocket):
    while True:
        my_sockets.broadcast_message("who is up")
        globals.logger.info(str(my_sockets.connected_computers))
        time.sleep(5)


def start_broadcast_setup(my_sockets: MultiSocket, sql_client: SQLClient, host_client: HostClient):
    my_sockets.broadcast_message(
        f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")
    threading.Thread(target=broadcast, args=(my_sockets,)).start()
    threading.Thread(target=handle_broadcast_answer, args=(my_sockets, sql_client, host_client)).start()
    print("Started Broadcasting")
