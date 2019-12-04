"""
Referencias: https://pymotw.com/3/socket/tcp.html
"""

import sys, os, socket, numpy, threading, _thread
from pycolor import *
from common import Get_Socket_Path

LOCK = threading.Lock()

server_path = Get_Socket_Path()
listen_IP = "127.0.0.8"
listen_port = 6000
BUFFER_SIZE = 4096    # N° bites máximo buffer (4 Kb)
ENCODING = "utf-8"    # utf-8 para poner tildes y caracteres extraños

DATABASE = { 0:   1001,
             1:   -15,
             3:   3.14159,
             930: "p" }

parlanchín_mode = True    # imprime lo que hace, si es True. Es como el flag genérico -v, -verbose


def Get_Printable_DB():
	stringed = "\n"
	try:
		import tabulate    # tratando de imprimir bonito con librería tabulate
		temp = [("Key", "Value", "ValType")]
		for key in DATABASE.keys():
			temp.append( (key, DATABASE[key], str(type(DATABASE[key])).split("\'")[1]) )
		stringed += tabulate.tabulate(temp)
	except Exception as e:
		#print("[TEST]", e)
		stringed += "\tKey\tValue\tValType\n"
		for key in DATABASE.keys():
			stringed += "\t%d\t%s\t%s\n" % (key, str(DATABASE[key]), str(type(DATABASE[key])).split("\'")[1])
	return stringed


def CheckError_Syntax(request_msj):     # si está mal, retorna True
	"""
		<command>\n
		[other_parms]
	"""
	_msjlines = request_msj.split("\n")[:-2]   # no pesca la última línea vacía
	if (len(_msjlines) == 1): return False
	if (len(_msjlines) > 1):
		_extra_parms_lst = _msjlines[1:]
		valid_parmNames = ["Host port", "Server port",  # de connect
		                   "Key", "Value", "ValType"]   # de varios
		for item in _extra_parms_lst:
			try: _parm_name = item.split(":")[0]
			except: return True
			if (_parm_name in valid_parmNames):
				valid_parmNames.remove(_parm_name)    # removiendo para verificar que no salga repetido un parámetro
			else:     # parámetro repetido o no reconocido
				return True
	return False


""" ES NECESARIO CREAR UNA LISTA DE BUFFER, PARA TENER UN BUFFER POR CLIENTE, PARA QUE NO COLISIONEN """
	
def Attend_Client_Request(conn):
	"""
	Función que emplean los threads del servidor para cada cliente.
	"""
	
	# se inicia siempre y cuando se haya conectado al cliente, así que lo primero que hace es enviarle la confirmación de conexión
	conn.send( "Connection successful (code: 0)\nBody:".encode(ENCODING) )  # caso especial de respuesta, digamos.
	
	while (True):  # ciclo para atender solicitudes del cliente hasta que se canse, o provoque error.
		while (LOCK.locked()): continue    # espera ocupada hasta que el cliente desbloquee el LOCK (deje de escribir en la base de datos).
		BUFFER = conn.recv(BUFFER_SIZE).decode(ENCODING)     # se queda esperando a recibir mensaje de cliente.
		while (LOCK.locked()): continue
		
		status_code = 0   # código_de_estado
		status_msj  = ""  # mensaje_de_estado
		body = ""         # mensaje_servidor
		
		if (parlanchín_mode): print("Server thread #%d just received: \'%s\'" % (_thread.get_ident(), BUFFER))
		
		if (CheckError_Syntax(BUFFER)):
			status_code = 200
			status_msj  = "Bad request syntax"
		
		else:
			lines = BUFFER.split("\n")
			#if (parlanchín_mode): print("[test]", lines)
			clientCMD = lines[0].lower()
			if (len(lines) >= 2):
				other_parms = {}       # other_parms es un diccionario con extras como "Key", "Value".
				for k in range(1, len(lines)):
					if (lines[k] == ""): continue
					if (": " in lines[k]): splitted = lines[k].split(": ")     # posibilitando UN espacio entre nombre de parámetro y valor del parámetro
					else: splitted = lines[k].split(":")                       # posibilitando que no haya espacio
					other_parms[splitted[0]] = splitted[1]
						
			if (clientCMD == "connect"):  # resuelto en el cliente porque antes de inicializar la conexión no puede pedirle al servidor conectarse. Se debe hacer en client.py
				pass
			
			
			elif (clientCMD == "disconnect"):
				conn.close()
			
			
			elif (clientCMD == "quit"):
				if (parlanchín_mode): PrintInfo("Client disconnected from server thread #%d" % (_thread.get_ident())
				return   # CERRAR THREAD ==> RETORNAR
			
			
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

				LOCK.acquire()
				DATABASE[newkey] = other_parms["Value"]
				LOCK.release()
					
			
			elif (clientCMD == "get"):   # ~ get(<key>)
				if (not "Key" in other_parms.keys()):
					status_code = 201
					status_msj  = "Bad parameters"
			
				if (other_parms["Key"] in DATABASE.keys()):
					status_code = 2
					status_msj  = "Get successful"
					body        = DATABASE[other_parms["Key"]]
				else:   # llave no existente en BD, error.
					status_code = 106
					status_msj  = "Bad key read"
			
			
			elif (clientCMD == "peek"):
				if ("Key" not in other_parms.keys()):
					status_code = 201
					status_msj  = "Bad parameters"
				else:
					try:
						_key = int(other_parms["Key"])
						assert(_key >= 0)
						error = False
					except:
						status_code = 105
						status_msj  = "Evil key"
						error = True
					if (not error):
						status_code = 3
						status_msj  = "Peek successful"
						body        = other_parms["Key"] in DATABASE.keys()
			
			
			elif (clientCMD == "update"):
				if ("Key" not in other_parms.keys()):
					status_code = 106
					status_msj  = "Bad key read"
				
				try:
					_key = int(other_parms["Key"])
					assert(_key >= 0)
					error = False
				except:
					status_code = 105
					status_msj  = "Evil key"
					error = True
				
				if (not error):
					if (other_parms["Key"] in DATABASE.keys()):   # llave en BD
						LOCK.acquire()
						DATABASE[other_parms["Key"]]
						LOCK.release()
						status_code = 5
						status_msj  = "Update successful"
					else:   # llave no existente en BD, error.
						status_code = 107
						status_msj  = "Bad key write"
					body = ""
			
			elif (clientCMD == "delete"): pass
			
			elif (clientCMD == "list"):
				status_code = 4
				status_msj  = "List successful"
				body = Get_Printable_DB()
			
			else:
				status_code = 104
				status_msj  = "Evil command"     # comando malvado.
		
		LOCK.acquire()
		answer = "%s (code: %d)\nBody:%s" % (status_msj, status_code, body)
		conn.send( answer.encode(ENCODING) )
		LOCK.release()

	conn.close()


SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
SOCK.bind((listen_IP, listen_port))

SOCK.listen(5)

while (True):     # ciclo hasta que el cliente quiera salirse
	if (parlanchín_mode): print("Server thread #%d awaiting connection..." % _thread.get_ident())
	connection_socket, client_address = SOCK.accept()
	if (parlanchín_mode): PrintInfo("Server thread #%d connected successfuly with client with IP %s on port %d (given by OS)" % (_thread.get_ident(), client_address[0], client_address[1]))
	_thread.start_new_thread(Attend_Client_Request, (connection_socket,))
SOCK.close()

#server_threads = []  ...
#server_threads.append( threading.Thread(target=Process_Client_Request, args=()) )
#server_threads[-1].start()

