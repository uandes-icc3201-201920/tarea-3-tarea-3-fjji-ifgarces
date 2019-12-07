"""
Referencias: https://pymotw.com/3/socket/tcp.html
"""

import sys, os, socket, numpy, threading, _thread
from pycolor import *
from common import Get_Wanted_IP

LOCK = threading.Lock()

listen_IP = Get_Wanted_IP()
listen_port = 6000
BUFFER_SIZE = 4096    # N° bites máximo buffer (4 Kb)
ENCODING = "utf-8"    # utf-8 para poner tildes y caracteres extraños

DATABASE = { 0:   1001,
             1:   -15,
             3:   3.14159,
             930: "p" }

parlanchín_mode = True    # imprime lo que hace, si es cierto.
# parlanchín_mode = ("-v" in sys.argv) or ("-verbose" in sys.argv)    # como de costumbre, el flag genérico para que el programa diga lo que está haciendo.


def Get_Printable_DB():
	stringed = "\n"
	try:
		import tabulate    # tratando de imprimir bonito con librería tabulate
		temp = [("Key", "Value", "ValType")]
		for key in DATABASE.keys():
			temp.append( (key, DATABASE[key], str(type(DATABASE[key])).split("\'")[1]) )
		stringed += tabulate.tabulate(temp)
	except:
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
		valid_parmNames = ["Host port", "Server port",  # de comando 'connect'
		                   "Key", "Value", "ValType"]   # de varios
		for item in _extra_parms_lst:
			try: _parm_name = item.split(":")[0]
			except: return True
			if (":" not in item): return True
			if (_parm_name in valid_parmNames):
				valid_parmNames.remove(_parm_name)    # removiendo para verificar que no salga repetido un parámetro
			else: return True    # parámetro repetido o no reconocido
	return False


""" [!] POSIBLE CONDICIÓN DE CARRERA POR 'BUFFER':
        Si el thread server t1 procesa instrucción y llena el buffer,
		es posible que ahora le toque a otro thread t2 y modifique el buffer,
		y reanude t1 con el buffer modificado por t2, y le envíe cualquier
		cosa al cliente.
		Será necesario poner un LOCK para todo Attend_Client_Request()?
"""

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
		_abort = False
		
		if (parlanchín_mode): print("Server thread #%d just received: \'%s\'" % (_thread.get_ident(), BUFFER))
		
		if (CheckError_Syntax(BUFFER)):
			status_code = 200
			status_msj  = "Bad request syntax"
		
		else:
			try:
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
			except:
				status_code = 200
				status_msj  = "Bad request syntax"
				_abort = True
				
			if (not _abort):
				if (clientCMD == "connect"):  # resuelto en el cliente porque antes de inicializar la conexión no puede pedirle al servidor conectarse. Se debe hacer en client.py
					pass
				
				
				elif (clientCMD == "disconnect"):
					conn.send( "Disconnection successful (code: 7)\nBody:".encode(ENCODING) )
					conn.close()
					break
				
				
				elif (clientCMD == "quit"):
					try: conn.close()
					except: pass
					if (parlanchín_mode):
						PrintInfo("Client disconnected from server thread #%d" % (_thread.get_ident()))
					return   # CERRAR THREAD ==> RETORNAR
				
				
				elif (clientCMD == "insert"):
					if ("Key" in other_parms.keys()):  # ~ insert(<key>, <value>)
						try:
							_key = int(other_parms["Key"])
							assert(_key >= 0)
							error = False
						except:
							status_code = 105
							status_msj  = "Evil key"
							error = True
						if (not error):			
							if (_key in DATABASE.keys()):
								status_code = 108
								status_msj  = "Bad key overload"
							else:   # llave no existente en BD, error.
								status_code = 1
								status_msj  = "Insert successful"
					
					else:   # ~ insert(<value>)
						_key = max(DATABASE.keys()) + 1
						status_code = 1
						status_msj  = "Insert successful"

					LOCK.acquire()
					try: DATABASE[_key] = int(other_parms["Value"])
					except: DATABASE[_key] = other_parms["Value"]
					LOCK.release()
						
				
				elif (clientCMD == "get"):   # ~ get(<key>)
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
							if (_key in DATABASE.keys()):
								status_code = 2
								status_msj  = "Get successful"
								body        = str( DATABASE[_key] )
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
							body        = str( _key in DATABASE.keys() )
				
				
				elif (clientCMD == "update"):
					if ("Key" not in other_parms.keys() or "Value" not in other_parms.keys()):
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
							if (_key in DATABASE.keys()):   # llave en BD
								LOCK.acquire()
								try: DATABASE[_key] = int(other_parms["Value"])
								except: DATABASE[_key] = other_parms["Value"]
								LOCK.release()
								status_code = 5
								status_msj  = "Update successful"
							else:   # llave no existente en BD, error.
								status_code = 107
								status_msj  = "Bad key write"
							body = ""
				
				elif (clientCMD == "delete"):
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
							if (_key in DATABASE.keys()):   # llave en BD
								LOCK.acquire()
								del DATABASE[_key]
								LOCK.release()
								status_code = 6
								status_msj  = "Delete successful"
							else:   # llave no existente en BD, error.
								status_code = 107
								status_msj  = "Bad key write"
							body = ""
				
				elif (clientCMD == "list"):
					status_code = 4
					status_msj  = "List successful"
					body = Get_Printable_DB()
				
				else:
					status_code = 104
					status_msj  = "Evil command"     # comando malvado.
		
		LOCK.acquire()
		answer = "%s (code: %d)\nBody: %s" % (status_msj, status_code, body)
		try:
			conn.send( answer.encode(ENCODING) )
		except Exception as e:
			if (parlanchín_mode):
				PrintError("[!] Error: send failed. Details: %s" % str(e))
			LOCK.release()
			break
		LOCK.release()

	conn.close()
	if (parlanchín_mode): print("Server thread #%d terminated.\n" % _thread.get_ident())


SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
SOCK.bind((listen_IP, listen_port))

SOCK.listen(5)    # [?] Necesario argumento de listen?

while (True):     # ciclo hasta que el cliente quiera salirse
	if (parlanchín_mode): print("\nServer thread #%d awaiting connection..." % _thread.get_ident())
	connection_socket, client_address = SOCK.accept()
	if (parlanchín_mode): PrintGoodNews("\nServer thread #%d connected successfuly with client with IP %s on port %d (given by OS)" % (_thread.get_ident(), client_address[0], client_address[1]))
	_thread.start_new_thread(Attend_Client_Request, (connection_socket,))
SOCK.close()


