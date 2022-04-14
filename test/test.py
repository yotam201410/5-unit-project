import subprocess
import threading
import time

# for i in range(255):
#     threading.Thread(target=lambda x: subprocess.call(['ping', '-n', '1', '-w', '100', '192.168.1.' + str(i)]),
#                      args=(i,)).start()
# time.sleep(5)
# arpa = subprocess.check_output(("arp", "-a")).decode("ascii")
# n_devices = [x for x in arpa.split('\n') if '192.168.1.' in x and
#              all(y not in x for y in ['192.168.1.1 ', '192.168.1.255'])]
from Code.NetworkTalk.Computer import Computer
from Code.NetworkTalk.MultiSocket import MultiSocket
from Code import globals
import re
import uuid
import socket
from Code.NetworkTalk.constants import Constants
import netifaces

l = []


def send_ping(ip):
    subprocess.call(['ping', '-n', '1', '-w', '100', ip])
    globals.logger.debug(f"sent ping to {ip}")


def start_discovery(my_sockets: MultiSocket):
    for first_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[0])):
        for second_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[1])):
            for third_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[2])):
                for forth_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[3])):
                    l.append(f"{255 - first_number}.{255 - second_number}.{255 - third_number}.{255 - forth_number}")
                    threading.Thread(target=send_ping,
                                     args=(
                                         f"{255 - first_number}.{255 - second_number}.{255 - third_number}.{255 - forth_number}",)).start()

    time.sleep(5)
    arpa = subprocess.check_output(("arp", "-a")).decode("ascii")
    n_devices = [x for x in arpa.split('\n') if '192.168.1.' in x and
                 all(y not in x for y in ['192.168.1.1 ', '192.168.1.255'])]

for i in netifaces.interfaces():
    try:
        addrs = netifaces.ifaddresses(i)
    except :
        continue


# my_computer = Computer(ip="192.168.1.105",
#                        mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
#                        port=Constants.listening_server_port, subnet_mask="255.255.255.0")
# my_sockets = MultiSocket(my_computer)
# start_discovery(my_sockets)
