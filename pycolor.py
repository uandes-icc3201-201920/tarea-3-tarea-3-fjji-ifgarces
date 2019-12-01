try:
	import colorama as color
	boring_user = False
	import platform
	if (platform.system().lower() != "linux"):
		color.init(convert=True)    # si se ejecuta en Windows, requiere esto para funcionar bien
	del platform
except:
	boring_user = True

def PrintError(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTRED_EX, text, color.Fore.RESET, sep="")

def PrintInfo(text):
	if (boring_user): print(text)
	else: print(color.Fore.YELLOW, text, color.Fore.RESET, sep="")

if (__name__ == "__main__"):
	if (not boring_user):
		print(color.Fore.RED, "YOU", color.Fore.RESET, sep="")
		print(color.Fore.YELLOW, "HAVE", color.Fore.RESET, sep="")
		print(color.Fore.BLUE, "THE POWER", color.Fore.RESET, sep="")
		print(color.Fore.GREEN, "OF", color.Fore.RESET, sep="")
		print(color.Back.CYAN, color.Fore.WHITE, "COLORS", color.Back.RESET, color.Fore.RESET, sep="")
	else:
		print("You do not have colorama instlled. You have nothing.")