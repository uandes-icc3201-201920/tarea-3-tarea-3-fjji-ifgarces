import sys
from pycolor import PrintError

def Get_Wanted_IP():
	_ip = ""   # internet dice que debe ser vacío para permitir que otros computadores se conecten...
	for k in range(len(sys.argv)):     # obteniendo ruta personalizada para el socket
		if (sys.argv[k][0] == "-"):
			if (sys.argv[k].lower() == "-s"):
				_ip = sys.argv[k+1]
				break
			else:
				PrintError("[!] Error: flag \'%s\' no reconocido." % cmdarg)
	return _ip