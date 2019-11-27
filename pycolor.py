try:
	import colorama as color
	boring_user = False
	import platform
	if (platform.system().lower() != "linux"):
		color.init(convert=True)
except:
	boring_user = True


def PrintError(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTRED_EX, text, color.Fore.RESET, sep="")
	exit(1)

def PrintInfo(text):
	if (boring_user): print(text)
	else: print(color.Fore.CYAN, text, color.Fore.RESET, sep="")

if (__name__ == "__main__"):	
	PrintInfo("Testing this.")