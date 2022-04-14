import socket
import subprocess
import threading
import time
from Code import globals

from Code.NetworkTalk import MultiSocket


def send_ping(ip):
    subprocess.call(['ping', '-n', '1', '-w', '100', ip])
    globals.logger.debug(f"sent ping to {ip}")


def start_discovery(my_sockets: MultiSocket):
    for first_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[0])):
        for second_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[1])):
            for third_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[2])):
                for forth_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[3])):
                    threading.Thread(target=send_ping,
                                     args=(f"{first_number}.{second_number}.{third_number}.{forth_number}",)).start()

    time.sleep(5)
    arpa = subprocess.check_output(("arp", "-a")).decode("ascii")
    n_devices = [x for x in arpa.split('\n') if '192.168.1.' in x and
                 all(y not in x for y in ['192.168.1.1 ', '192.168.1.255'])]
