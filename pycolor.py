""" pycolor: nombre inventado. Así debería llamarse colorama mejor, porque yo lo digo. """

try:
	import colorama as color
	boring_user = False
	import platform
	if (platform.system().lower() != "linux"):
		color.init(convert=True)    # si se ejecuta en Windows, requiere esto para funcionar bien
	del platform
except:
	boring_user = True

def PrintError(text):      # rojo = malo.
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTRED_EX, text, color.Fore.RESET, sep="")

def PrintInfo(text):       # imprime info destacada, en amarillo.
	if (boring_user): print(text)
	else: print(color.Fore.YELLOW, text, color.Fore.RESET, sep="")

def PrintGoodNews(text):   # verde = bueno.
	if (boring_user): print(text)
	else: print(color.Fore.GREEN, text, color.Fore.RESET, sep="")

if (__name__ == "__main__"):
	if (not boring_user):
		print(color.Fore.RED,    "YOU ",       sep="", end="")
		print(color.Fore.YELLOW, "HAVE ",      sep="", end="")
		print(color.Fore.BLUE,   "THE POWER ", sep="", end="")
		print(color.Fore.GREEN,  "OF ",        sep="", end="")
		print(color.Back.CYAN, color.Fore.WHITE, "COLORS\n", color.Back.RESET, color.Fore.RESET, sep="", end="")
	else:
		print("You do not have colorama library instlled. You have nothing.")
		print("Do you want me to install it for you? (y/n)  ", end="")
		if (input().lower() not in ["y", "yes"]):
			print("...")
			exit(0)
		print("Trying to install...")
		try:
			# https://stackoverflow.com/questions/12937533/use-pip-install-uninstall-inside-a-python-script
			from pip._internal import main as pipmain
			pipmain.main(["install", "colorama"])
			print(color.Back.CYAN, color.Fore.WHITE, " Yay! It worked. \n", color.Back.RESET, color.Fore.RESET, sep="", end="")
		except:
			print("I have failed to install it, probably because you have Python 2 or lower.")
