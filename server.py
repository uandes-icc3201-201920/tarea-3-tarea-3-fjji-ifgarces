import sys
import numpy.random as rand
from KVclass import *

try:
	import colorama as color
	color.init(convert=True)
	boring_user = False
except:
	boring_user = True


def PrintError(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTRED_EX, text, color.Fore.RESET)
	exit(-1)

def PrintYellow(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTYELLOW_EX, text, color.Fore.RESET)

socket_path = "/tmp/db.tuples.sock"
for k in range(len(sys.argv)):     # obteniendo ruta personalizada para el socket
	if (sys.argv[k][0] == "-"):
		if (sys.argv[k].lower() == "-s"):
			socket_path = sys.argv[k+1]
			break
		else:
			PrintError("[!] Error: flag \'%s\' no reconocido." % cmdarg)

