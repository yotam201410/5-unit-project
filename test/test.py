# import subprocess
# import threading
# import time
#
# # for i in range(255):
# #     threading.Thread(target=lambda x: subprocess.call(['ping', '-n', '1', '-w', '100', '192.168.1.' + str(i)]),
# #                      args=(i,)).start()
# # time.sleep(5)
# # arpa = subprocess.check_output(("arp", "-a")).decode("ascii")
# # n_devices = [x for x in arpa.split('\n') if '192.168.1.' in x and
# #              all(y not in x for y in ['192.168.1.1 ', '192.168.1.255'])]
# from Code.NetworkTalk.Computer import Computer
# from Code.NetworkTalk.MultiSocket import MultiSocket
# from Code import globals
# import re
# import uuid
# import socket
# from Code.NetworkTalk.constants import Constants
# import netifaces
#
# l = []
#
#
# def send_ping(ip):
#     subprocess.call(['ping', '-n', '1', '-w', '100', ip])
#     globals.logger.debug(f"sent ping to {ip}")
#
#
# def start_discovery(my_sockets: MultiSocket):
#     for first_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[0])):
#         for second_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[1])):
#             for third_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[2])):
#                 for forth_number in range(256 - int(my_sockets.computer.subnet_mask.split('.')[3])):
#                     l.append(f"{255 - first_number}.{255 - second_number}.{255 - third_number}.{255 - forth_number}")
#                     threading.Thread(target=send_ping,
#                                      args=(
#                                          f"{255 - first_number}.{255 - second_number}.{255 - third_number}.{255 - forth_number}",)).start()
#
#     time.sleep(5)
#     arpa = subprocess.check_output(("arp", "-a")).decode("ascii")
#     n_devices = [x for x in arpa.split('\n') if '192.168.1.' in x and
#                  all(y not in x for y in ['192.168.1.1 ', '192.168.1.255'])]
#
# for i in netifaces.interfaces():
#     try:
#         addrs = netifaces.ifaddresses(i)
#     except :
#         continue
#
#
# # my_computer = Computer(ip="192.168.1.105",
# #                        mac=':'.join(re.findall('..', '%012x' % uuid.getnode())), name=socket.gethostname(),
# #                        port=Constants.listening_server_port, subnet_mask="255.255.255.0")
# # my_sockets = MultiSocket(my_computer)
# # start_discovery(my_sockets)

import socket

import ssl

import certifi

import os
from OpenSSL import crypto, SSL


def cert_gen(
        emailAddress="emailAddress",
        commonName="commonName",
        countryName="NT",
        localityName="localityName",
        stateOrProvinceName="stateOrProvinceName",
        organizationName="organizationName",
        organizationUnitName="organizationUnitName",
        serialNumber=0,
        validityStartInSeconds=0,
        validityEndInSeconds=10 * 365 * 24 * 60 * 60,
        KEY_FILE="server.key",
        CERT_FILE="server.crt"):
    # can look at generated file using openssl:
    # openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))


cert_gen()
# Create a place holder to consolidate SSL settings

# i.e., Create an SSLContext
server_socket = socket.socket()
server_socket.bind(("127.0.0.1", 7000))
server_socket = ssl.wrap_socket(server_socket, cert_reqs=ssl.CERT_NONE, server_side=True, keyfile="server.key",
                                certfile="server.crt")
