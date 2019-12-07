import sys
from pycolor import PrintError

"""
---- INFO ----
  El enunciado decía que la flag indicaba ruta (i.e. /tmp/etc.) pero eso no tiene sentido,
  así que asumo que se equivocaron. La ruta no interesa para internet. Al menos en este caso no.
"""

def Get_Wanted_IP():
	_ip = ""   # internet dice que debe ser vacío para permitir que otros computadores se conecten...
	for k in range(len(sys.argv)):   # obteniendo dirección IP personalizada para el socket (del servidor, porque en el cliente el comando connect lo especifica aparte)
		if (sys.argv[k][0] == "-"):
			if (sys.argv[k].lower() == "-s"):
				_ip = sys.argv[k+1]
				break
			else:
				PrintError("[!] Error: flag \'%s\' no reconocido." % sys.argv[k])
				exit(1)
	return _ip