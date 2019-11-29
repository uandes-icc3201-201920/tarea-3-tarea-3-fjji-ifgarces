import sys, os, socket
from pycolor import *
from common import Get_Socket_Path

def ShowHelp():
	PrintInfo("[Ayuda]\nDigite la instrucción del cliente de acuerdo al protocolo definido (request). Para terminar de escribir y enviar el mensaje, ingrese una línea vacía.\n")


def main():
	host_path = Get_Socket_Path()
	#host_IP = "127.0.0.8"
	#host_port = 6000
	#client_port = 6891  # UNUSED (dado por el S.O.)
	BUFFER_SIZE = 4096
	ENCODING = "utf-8"

	BUFFER = ""
	isConnected = False
	
	#ShowHelp()
	
	while (True):
		BUFFER = ""
		_aux = input("\n  > ")
		if (_aux.replace(" ", "") == ""): continue
		while (_aux.replace(" ", "") != ""):
			BUFFER += _aux + "\n"
			_aux = input("... ")
		
		instructions = BUFFER.split("\n")
		userCMD = instructions[0].replace(" ", "").lower()
		
		if (userCMD == "connect"):
			if (isConnected):
				print("Ud. ya se encuentra conectado al servidor.")
			
			try:
				if (instructions[1].lower() == "quick"): host_IP = "127.0.0.8"; host_port = 6000   # testing only!!
				else:
					host_IP = instructions[1].split(": ")[1]
					if (host_IP.lower() == "default"): host_IP = "127.0.0.8"
					host_port = int( instructions[2].split(": ")[1] )
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.connect((host_IP, host_port))
				isConnected = True
			except Exception as e:
				PrintError("[!] Error: no se pudo conectar al servidor o no siguió la sintaxis adecuada.")
				print("Detalles del error: ", e)
		
		elif (userCMD == "quit"):
			if (isConnected):
				connection.send(BUFFER.encode(ENCODING))
				connection.close()
				isConnected = False
			exit(0)
		
		elif (userCMD == "disconnect"):
			if (not isConnected):
				print("Ud. no se encuentra conectado al servidor.")
				continue
			connection.send(BUFFER.encode(ENCODING))
			connection.close()
			PrintInfo("Ud. se ha desconectado del servidor")
			isConnected = False
		
		else:
			if (isConnected): connection.send(BUFFER.encode(ENCODING))
			else: PrintError("[!] Error: no está actualmente conectado al servidor. Primero ejecute comando \'connect\'")
		""" en este punto envió el request """
		
		""" ahora espera el response del servidor... """
		if (isConnected):
			BUFFER = connection.recv(BUFFER_SIZE).decode(ENCODING)
			PrintInfo("Client just received: \'%s\'" % BUFFER)

if (__name__ == "__main__"):
    main()

