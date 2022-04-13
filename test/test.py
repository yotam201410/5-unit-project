import socket

_broadcast_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
_broadcast_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
_broadcast_send_socket.sendto("sok,AF:DF,3000,idk,up".encode(), ("255.255.255.255", 4000))
