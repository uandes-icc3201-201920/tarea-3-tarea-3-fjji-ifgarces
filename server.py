"""
https://docs.python.org/3.6/library/socket.html#module-socket
"""

import sys, os, socket, numpy, threading
from KVclass import *
from pycolor import *


server_path = "/tmp/db.tuples.sock"
listen_IP = "127.0.0.1"     # la que por defecto en los tutoriales de esto usan
listen_port = numpy.random.randint(5000, 9000)   # ??
BUFFER = ""
BUFFER_SIZE = 4096    # N° bites máximo buffer

for k in range(len(sys.argv)):     # obteniendo ruta personalizada para el socket
	if (sys.argv[k][0] == "-"):
		if (sys.argv[k].lower() == "-s"):
			server_path = sys.argv[k+1]
			break
		else:
			PrintError("[!] Error: flag \'%s\' no reconocido." % cmdarg)

if (os.path.exists(server_path)):  # borrando el socket si es que ya existía
	os.remove(server_path)


def Process_Client_Request():
	SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # inicializando socket de stream, por IP internet
	#SOCK.connect(listen_IP, listen_port)  ...?
	SOCK.bind((listen_IP, listen_port))  # SOCK.bind(server_path) ...?
	SOCK.listen()
	
	conn, addr = SOCK.accept()

	PrintInfo(addr)
	PrintInfo(conn)

	while (True):
		BUFFER = conn.recv(BUFFER_SIZE)     # se queda esperando a recibir mensaje de cliente
		if (BUFFER == ""): break
		PrintInfo("Read: " % BUFFER)
		
		client_cmd = BUFFER.split("\n")[0]
		# ...?
		
		answer = ""
		if ( <se quiere enviar algo binario> ): answer = b""
		# .....
		conn.send(answer)

	conn.close()

server_threads = []
#...
server_threads.append( threading.Thread(target=Process_Client_Request, args=()) )
server_threads[-1].start()