try:
	import colorama as color
	boring_user = False
except:
	boring_user = True


def PrintError(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTRED_EX, text, color.Fore.RESET)
	exit(1)

def PrintInfo(text):
	if (boring_user): print(text)
	else: print(color.Fore.LIGHTYELLOW_EX, text, color.Fore.RESET)