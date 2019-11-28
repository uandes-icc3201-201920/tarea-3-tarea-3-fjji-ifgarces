import sys, os, socket
from pycolor import *
from common import Get_Socket_Path


host_path = Get_Socket_Path()

host_IP = "127.0.0.8"
host_port = 6000
BUFFER_SIZE = 4096

cmd = ""
connected = 0

def Main():
	host_path = Get_Socket_Path()

	host_IP = "127.0.0.8"
	host_port = 6000
	BUFFER_SIZE = 4096

	cmd = ""
	connected = 0
	while (( cmd != "quit" )or(cmd != "disconnect")):
		if (connected == 1):
			PrintInfo("Estado: Conectado al Servidor\n")
		else:
			PrintInfo("Estado: Desconectado\n")
		if(cmd == "quit"):
			connection.close()
			connected = 0
			exit(0)
		cmd = input(">")
		if ( cmd =="connect"):
			connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# connect to server on local computer
			connection.connect((host_IP, host_port))
			connected = 1
			continue
		elif( cmd == "disconnect"):
			msg = "out" #poner el que corresponde
			connection.send(msg.encode('utf-8'))
			connection.close()
			PrintInfo("Usted se ha desconectado del servidor\n")
			connected = 0
			continue
	try:
		s.close()
	finally:
		pass


if __name__ == '__main__':
    Main()

def TEST():
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
