import sys
from pycolor import PrintError

def Get_Socket_Path():
	_path = "/tmp/db.tuples.sock"
	for k in range(len(sys.argv)):     # obteniendo ruta personalizada para el socket
		if (sys.argv[k][0] == "-"):
			if (sys.argv[k].lower() == "-s"):
				_path = sys.argv[k+1]
				break
			else:
				PrintError("[!] Error: flag \'%s\' no reconocido." % cmdarg)
	return _path