import time
import threading
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code import globals
from Code.NetworkTalk.constants import Constants


def handle_broadcast_answer(my_sockets: MultiSocket):
    while True:
        data, udp_addrees = my_sockets.udp_server_socket.recvfrom(1024)
        if udp_addrees[0] != my_sockets.computer.ip:
            splited_data = data.decode().split(',')
            if splited_data[-1] == "up":
                connected_computer = Computer(ip=splited_data[0], subnet_mask=splited_data[1], mac=splited_data[2],
                                              port=int(splited_data[3]), name=splited_data[4])
                my_sockets.add_server_sockets(connected_computer)
            elif splited_data[-1] == "who is up":
                if my_sockets.get_computer_from_ip_client_sockets(udp_addrees[0]) is None:
                    connected_computer = Computer(ip=udp_addrees[0], port=Constants.listening_server_port)
                    my_sockets.client_sockets[connected_computer] = None
                else:
                    pass
                my_sockets.broadcast_message(
                    f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")


def broadcast(my_sockets: MultiSocket):
    while True:
        my_sockets.broadcast_message("who is up")
        globals.logger.info("CLIENTS " + str(my_sockets.client_sockets))
        globals.logger.info("SERVERS " + str(my_sockets.server_sockets))

        time.sleep(30)


def start_broadcast_setup(my_sockets: MultiSocket):
    my_sockets.broadcast_message(
        f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")
    threading.Thread(target=broadcast, args=(my_sockets,)).start()
    threading.Thread(target=handle_broadcast_answer, args=(my_sockets,)).start()
