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

def Initialize_Server():
	DATABASE = { 0: 1001,
                 1: -15,
	             3: 3.14159265,
	             930: "p" }

	SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
	SOCK.bind((listen_IP, listen_port))


def CheckError_Syntax(request_msj):     # si está mal, retorna True
	"""
	0.	<command>\n
	1.	Host: <IP>\n
	2.	Client port: <portnum>\n
	3.	Server port: <portnum>\n
	4.	[other_parms]
	"""
	_msjlines = request_msj.split("\n")
	if (len(_msjlines) < 4): return True
	if (_msjlines[1].split(":")[0] != "Host"):        return True
	if (_msjlines[2].split(":")[0] != "Client port"): return True
	if (_msjlines[3].split(":")[0] != "Server port"): return True
	if (len(_msjlines) > 4):
		_other_parameters = _msjlines[4:]
		valid_parmNames = ["Key", "Value", "ValType"]
		for item in _other_parameters:
			if (item in valid_parmNames):
				valid_parmNames.remove(item)    # removiendo para verificar que no salga repetido un parámetro
			else:
				return True


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
		
		if (CheckError_Syntax(BUFFER)):
			status_code = 200
			status_msj  = "Bad request syntax"
		
		else:
			lines = BUFFER.split("\n")
			clientCMD = lines[0]
			_host     = lines[1]
			_CLIport  = lines[2]
			_SRVport  = lines[3]
			if (len(lines) > 4):
				other_parms = {}       # other_parms es un diccionario con extras como "Key", "Value".
				for k in range(4, len(lines)):
					splitted = lines[k].split(":")
					other_parms[splitted[0]] = splitted[1]
			
			status_code = 0   # código_de_estado
			status_msj  = ""  # mensaje_de_estado
			body = ""    # mensaje_servidor
			###if ( <se quiere enviar algo binario> ): status_msj = b""
			
			if (clientCMD == "connect"):
				connected = True
			
			elif (clientCMD == "disconnect"):
				connection_socket.close()
				connected = False
			
			elif (clientCMD == "quit"):
				return  # ... cerrar cliente
			
			elif (clientCMD == "insert"):
				if ("Key" in other_parms.keys()):   # ~ insert(<key>, <value>)
					if (type(other_parms["Key"] != int) or other_parms["Key"] < 0):     # llave mala
						status_code = 105
						status_msj  = "Evil key"
					elif (other_parms["Key"] in DATABASE.keys()):  # si ya existe dicha llave en la BD
						status_code = 108
						status_msj  = "Bad key overload"
					else:
						newkey = other_parms["Key"]
						status_code = 1
						status_msj  = "Insert successful"
				
				else:    # ~ insert(<value>)
					newkey = max(DATABASE.keys())+1
					status_code = 1
					status_msj  = "Insert successful"
				DATABASE[newkey] = other_parms["Value"]
					
			
			elif (clientCMD == "get"):   # ~ get(<key>)
				if (not "Key" in other_parms.keys()):
					status_code = 201
					status_msj  = "Bad parameters"
			
				if (other_parms["Key"] in DATABASE.keys()):
					status_code = 2
					status_msj  = "Get successful"
					body        = DATABASE[other_parms["Key"]]
				else:
					status_code = 106
					status_msj  = "Bad key read"
			
			elif (clientCMD == "peek"):
				if ("Key" not in other_parms.keys()):
					status_code = 201
					status_msj  = "Bad parameters"
				else:
					status_code = 3
					status_msj  = "Peek successful"
					body        = other_parms["Key"] in DATABASE.keys()
			
			elif (clientCMD == "update"):
				if ("Key" not in other_parms.keys()):
					status_code = 106
					status_msj  = "Bad key read"
			
			elif (clientCMD == "delete"): pass
			
			elif (clientCMD == "list"): pass
			
			else:
				status_code = 104
				status_msj = "Evil command"     # comando malvado.
		
		
		connection_socket.send( "%s (code: %d)\nBody:%s" % (status_msj, status_code, body) )

	connection_socket.close()

server_threads = []
#...
server_threads.append( threading.Thread(target=Process_Client_Request, args=()) )
server_threads[-1].start()

