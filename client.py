import sys, os, socket
from pycolor import *
from common import Get_Socket_Path


host_path = Get_Socket_Path()

host_IP = "127.0.0.8"
host_port = 6000
BUFFER_SIZE = 4096

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def TEST():
	print("Connecting to server in IP address {} in port {}...".format(host_IP, host_port))
	connection.connect((host_IP, host_port))
	
	print("Receiving expected hello...")
	BUFFER = connection.recv(BUFFER_SIZE)
	BUFFER = BUFFER.decode("utf-8")
	print("Received from server: %s" % BUFFER)
	
	print("Sending hello back...")
	connection.sendall("Hi, this is the client speaking.".encode("utf-8"))
	
	connection.close()
	print("I have closed the connection")

if ("TESTMODE" in sys.argv):
	TEST()
	exit()
