"""
https://pymotw.com/3/socket/tcp.html
"""

import sys, os, socket, numpy, threading
from pycolor import *
from common import Get_Socket_Path


server_path = Get_Socket_Path()

listen_IP = "127.0.0.1"     # la que por defecto en los tutoriales de esto usan
listen_port = 6000
BUFFER = b""
BUFFER_SIZE = 4096    # N° bites máximo buffer (4 Kb)

DATABASE = []



def Get_Printable_DB(KV_list):
	stringed = "\n"
	
	try:
		import tabulate    # tratando de imprimir bonito con librería tabulate
		temp = [("Key", "Value", "ValType")]
		for item in KV_list:
			temp.append()
		stringed += tabulate.tabulate(temp)
		del temp
		
	except:
		stringed += "Key\tValue\tValType\n"
		for item in KV_list:
			stringed += str(item) + "\n"
		
	return stringed


"""
def TEST():
	SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
	SOCK.bind((listen_IP, listen_port))  # SOCK.bind(server_path) ...?
	SOCK.listen()

	print("Waiting for connection...")
	connection, client_address = SOCK.accept()

	print("Client address: ", client_address)

	print("Sending hello...")
	connection.sendall(b'Hello there, I\'m the server.')

	BUFFER = connection.recv(BUFFER_SIZE)
	print("Received: ", BUFFER)
"""

def Initialize_server():
	DATABASE = { 0: 1001,
                 1: -15,
	             3: 3.14159265,
	             930: "p" }

	SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
	SOCK.bind((listen_IP, listen_port))
	


def Attend_Client_Request():     # función que emplean los threads del servidor para cada cliente.
	SOCK.listen()
	
	connection_socket, client_IP = SOCK.accept()    # se queda esperando a que un cliente se conecte.
	
	print("[test]", client_IP)
	print("[test]", connection_socket)
	print()
	
	while (True):    # ciclo para atender solicitudes del cliente hasta que se canse, o provoque error.
		BUFFER = connection_socket.recv(BUFFER_SIZE)     # se queda esperando a recibir mensaje de cliente.
		if (BUFFER == ""): break
		print("[test] Server just received: " % BUFFER)
		
		lines = BUFFER.split("\n")
		clientCMD = lines[0]
		_host     = lines[1]
		_CLIport  = lines[2]
		_SRVport  = lines[3]
		if (len(lines) > 4):
			_extra_parms = {}
			for k in range(4, len(lines)):
				splitted = lines[k].split(":")
				_extra_parms[splitted[0]] = splitted[1]
		
		status = 0   # código_de_estado
		answer = ""  # mensaje_de_estado
		body = ""    # mensaje_servidor
		###if ( <se quiere enviar algo binario> ): answer = b""
		
		if (clientCMD == "connect"):
			connected = True
		
		elif (clientCMD == "disconnect"):
			connection_socket.close()
			connected = False
		
		elif (clientCMD == "quit"):
			return  # ... cerrar cliente
		
		elif (clientCMD == "insert"):
			if ("Key" in _extra_parms.keys()):   # ~ insert(<key>, <value>)
				if (type(_extra_parms["Key"] != int) or _extra_parms["Key"] < 0):
					status = 105
					answer = "Evil key"
				elif (_extra_parms["Key"] in DATABASE):  # si ya existe dicha llave en la BD
					status = 108
					answer = "Bad key overload"
				else:
					newkey = _extra_parms["Key"]
			
			else:    # ~ insert(<value>)
				newkey = max(DATABASE.keys())+1
			DATABASE[newkey] = _extra_parms["Value"]
				
		
		elif (clientCMD == "get"): pass
		
		elif (clientCMD == "peek"): pass
		
		elif (clientCMD == "update"): pass
		
		elif (clientCMD == "delete"): pass
		
		elif (clientCMD == "list"): pass
		
		else:
			status = 104
			answer = "Evil command"     # comando malvado.
		
		
		connection_socket.send( "%s (code: %d)\nBody:%s" % (answer, status, body) )

	connection_socket.close()

server_threads = []
#...
server_threads.append( threading.Thread(target=Process_Client_Request, args=()) )
server_threads[-1].start()

