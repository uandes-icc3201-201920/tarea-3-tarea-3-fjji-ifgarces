import sys, os, socket, time, _thread
from pycolor import *
from common import Get_Wanted_IP

def Show_Help():
	PrintInfo("[Ayuda]\n"
			  + "Digite la instrucción del cliente de acuerdo al protocolo definido (request).\n"
			  + "Para terminar de escribir y enviar el mensaje, ingrese una línea vacía.\n"
			  + "El timeout para conectarse al servidor y el de respuesta de este son de 10 segundos ambos.\n")

isConnected = False
still_waiting_response = False
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def SelfDeath_Timeout():  # ejecutado por un thread que asesina al padre si no avanzó (se conectó al servidor) en un cierto tiempo
	""" no funciona, porque por algún motivo la variable isConnected no se sobreescribe...
	    Como si se copiara, como si fuera un proceso distinto en vez de un thread """
	time.sleep(15)
	if (not isConnected):    # en ese rato debería estar conectado. Si no, muere.
		print(" -- connection timeout -- ")
		print(isConnected)
		_thread.interrupt_main()


def Response_Timeout():
	time.sleep(5)        # le da 10 segundos al servidor para que responda
	if (still_waiting_response): print("La respuesta del servidor está tomando más del tiempo normal...")
	time.sleep(5)
	if (still_waiting_response):
		#_thread.interrupt_main()
		PrintError("[!] Timeout: tiempo máximo de respuesta del servidor excedido.")
		if (isConnected): connection.send( "quit\n\n".encode("utf-8") )
		connection.close()
		exit(1)


def main():
	host_IP = Get_Wanted_IP()
	# host_IP = "127.0.0.8"
	# host_port = 6000
	BUFFER_SIZE = 4096
	ENCODING = "utf-8"

	BUFFER = ""
	isConnected = False

	while (True):
		#if (not isConnected): _thread.start_new_thread(SelfDeath_Timeout, ())
				
		BUFFER = ""
		try:
			_aux = input("\n  > ")
			if (_aux.replace(" ", "") == ""): continue
			while (_aux.replace(" ", "") != ""):  # input termina al ingresar línea vacía (simplemente, tecla enter).
				BUFFER += _aux + "\n"
				_aux = input("... ")
		
		except KeyboardInterrupt as e:
			PrintError("[!] Timeout: el tiempo máximo para conectarse al servidor expiró.")
			exit(1)


		instructions = BUFFER.split("\n")
		userCMD = instructions[0].replace(" ", "").lower()

		if (userCMD == "connect"):
			if (isConnected):
				print("Oiga, ud. ya se encuentra conectado al servidor. Tranquilícese.")
				continue

			try:
				isConnected = True
				host_IP = instructions[1].split(": ")[1]
				if (host_IP.lower() == "default"): host_IP = "127.0.0.8"
				host_port = instructions[2].split(": ")[1]
				if (host_port.lower() == "default"):
					host_port = 6000
				else:
					host_port = int(host_port)
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				connection.connect((host_IP, host_port))
			except Exception as e:
				PrintError("[!] Error: no se pudo conectar al servidor o ud. no siguió la sintaxis adecuada.")
				print("Detalles del error: ", e)

		elif (userCMD == "quit"):
			if (isConnected):
				connection.send( BUFFER.encode(ENCODING) )
				connection.close()
				isConnected = False
				print("Se le ha desconectado del servidor automáticamente (use \'disconnect\' antes de \'quit\').")
			exit(0)

		elif (userCMD == "disconnect"):
			if (not isConnected):
				print("Ud. no se encuentra conectado al servidor actualmente.")
				continue
			connection.send( BUFFER.encode(ENCODING) )
			PrintInfo( connection.recv(BUFFER_SIZE).decode(ENCODING) )
			connection.close()
			isConnected = False

		elif (userCMD == "help" or userCMD == "ayua"):	# EXTRA
			Show_Help();	   # todo buen programa debe tener su flag o comando de ayuda. Puntos extra.
			continue

		else:
			if (isConnected):
				connection.send( BUFFER.encode(ENCODING) )
			else:
				PrintError("[!] Error: no está actualmente conectado al servidor. "
						   + "Ejecute comando \'connect\' antes de ejecutar otro.")
		""" en este punto envió el request """

		""" ahora espera la respuesta del servidor... """
		if (isConnected):
			still_waiting_response = True
			_thread.start_new_thread(Response_Timeout, ())
			
			BUFFER = connection.recv(BUFFER_SIZE).decode(ENCODING)
			
			still_waiting_response = False
			#print("Respuesta recibida del servidor: ")
			PrintInfo("%s" % BUFFER)


if (__name__ == "__main__"):
	main()
