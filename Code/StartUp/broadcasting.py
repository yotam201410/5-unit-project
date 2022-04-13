import time
import threading
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code import globals

def add_computer_from_answer(computer: Computer, my_sockets: MultiSocket):
    sending_socket, tcp_address = my_sockets.receiving_socket.accept()
    my_sockets.add_computer(computer=computer, client_socket=sending_socket)


def handle_broadcast_answer(my_sockets: MultiSocket):
    while True:
        data, udp_address = my_sockets.udp_server_socket.recvfrom(1024)  # port here randomly generated
        splited_data = data.decode().split(',')
        print(data.decode())
        if "up" == splited_data[-1] and splited_data[0] != my_sockets.computer.ip:
            globals.logger.debug(f"recived up message '{data.decode()}'")
            ip, mac, port, name = splited_data[0], splited_data[1], int(splited_data[2]), splited_data[3]
            connected_computer = Computer(ip=ip, mac=mac, port=port, name=name)
            threading.Thread(target=add_computer_from_answer, args=(connected_computer, my_sockets)).start()
        elif splited_data == "who is up" and my_sockets.computer.ip:
            my_sockets.broadcast_message(f"{my_sockets.computer.ip},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")


def broadcast(my_sockets: MultiSocket):
    while True:
        my_sockets.broadcast_message("who is up")
        time.sleep(0.25)


def start_broadcast_setup(my_sockets: MultiSocket):
    my_sockets.broadcast_message(
        f"{my_sockets.computer.ip},{my_sockets.computer.mac},{my_sockets.computer.port},{my_sockets.computer.name},up")
    threading.Thread(target=broadcast, args=(my_sockets,)).start()
    threading.Thread(target=handle_broadcast_answer, args=(my_sockets,)).start()
