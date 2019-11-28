import sys, os, socket
from pycolor import *
from common import Get_Socket_Path

"""
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
if ("TEST" in sys.argv): PrintInfo("TEST MODE ENABLED"); TEST(); exit()
"""

def ShowHelp():
	PrintInfo("[Ayuda]\nDigite la instrucción del cliente de acuerdo al protocolo definido (request). Para terminar de escribir y enviar el mensaje, ingrese una línea vacía.")


def main():
	host_path = Get_Socket_Path()
	host_IP = "127.0.0.8"
	host_port = 6000
	BUFFER_SIZE = 4096
	ENCODING = "utf-8"

	msj = ""
	isConnected = False
	
	ShowHelp()
	
	while (True):
		msj = ""
		_aux = input("  > ")
		while (_aux.replace(" ", "") != ""):
			msj += _aux
			_aux = input("... ")
			
		
		userCMD = msj.split("\n")[0]
		
		if (userCMD == "connect"):
			if (isConnected):
				print("Ud. ya se encuentra conectado al servidor.")
			try:
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.connect((host_IP, host_port))
				isConnected = True
			except:
				PrintError("[!] Error: no se pudo conectar al servidor. Asegúrese de que está ejecutándose.")
		
		elif (userCMD == "quit"):
			connection.send(msj.encode(ENCODING))
			if (isConnected):
				connection.close()
				isConnected = False
			exit(0)
		
		elif (userCMD == "disconnect"):
			connection.send(msj.encode(ENCODING))
			connection.close()
			PrintInfo("Usté se ha desconectado del servidor\n")
			isConnected = False
		
		else:
			connection.send(msj.encode(ENCODING))
		
		#connection.recv(BUFFER_SIZE).decode(ENCODING)


if (__name__ == "__main__"):
    main()

