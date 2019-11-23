import sys, os, socket
from pycolor import *
from common import Get_Socket_Path


host_path = Get_Socket_Path()

host_IP = "127.0.0.1"
host_port = 6000
host_URL = "theserver.com ??"   # ???
BUFFER = b""
BUFFER_SIZE = 4096

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PrintInfo("Hi there")

SOCK.close()

"""
def TEST()
	print("Connecting to server in IP address {} in port {}...".format(host_IP, host_port))
	SOCK.connect((host_IP, host_port))

	print("Receiving expected hello...")
	BUFFER = SOCK.recv(BUFFER_SIZE)
	print("Received from server: %s" % BUFFER)

	print("Sending hello back...")
	SOCK.sendall(b'Hi, this is the client speaking.')

	SOCK.close()
"""
