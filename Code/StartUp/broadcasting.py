import time
import threading
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code import globals


def handle_broadcast_answer(my_sockets: MultiSocket):
    while True:
        data, udp_address = my_sockets.udp_server_socket.recvfrom(1024)  # port here randomly generated
        splited_data = data.decode().split(',')
        if udp_address[0] != my_sockets.computer.ip:
            print(data.decode())
        if "up" == splited_data[-1] and udp_address[0] != my_sockets.computer.ip:
            globals.logger.info(f"received 'up' BROADCAST message '{data.decode()}'")
            ip, subnet_mask, mac, port, name = splited_data[0], splited_data[1], splited_data[2], int(splited_data[3]), \
                                               splited_data[4]
            connected_computer = Computer(ip=ip, mac=mac, port=port, name=name, subnet_mask=subnet_mask)
            threading.Thread(target=my_sockets.add_server_sockets_or_update, args=(connected_computer,)).start()
        elif splited_data[-1] == "who is up" and my_sockets.computer.ip != udp_address[0]:
            globals.logger.info("received 'who is up' BROADCAST message")
            threading.Thread(target= my_sockets.broadcast_message(
                f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")).start()


def broadcast(my_sockets: MultiSocket):
    while True:
        my_sockets.broadcast_message("who is up")
        time.sleep(0.25)


def start_broadcast_setup(my_sockets: MultiSocket):
    my_sockets.broadcast_message(
        f"{my_sockets.computer.ip},{my_sockets.computer.subnet_mask},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")
    threading.Thread(target=broadcast, args=(my_sockets,)).start()
    threading.Thread(target=handle_broadcast_answer, args=(my_sockets,)).start()
