import sys, os, socket
from pycolor import *
from common import Get_Socket_Path


def ShowHelp():
    PrintInfo("[Ayuda]\n"
              + "Digite la instrucción del cliente de acuerdo al protocolo definido (request).\n"
              + "Para terminar de escribir y enviar el mensaje, ingrese una línea vacía.\n")


def main():
    host_IP = Get_Wanted_IP()
    # host_IP = "127.0.0.8"
    # host_port = 6000
    BUFFER_SIZE = 4096
    ENCODING = "utf-8"

    BUFFER = ""
    isConnected = False

    while (True):
        BUFFER = ""
        _aux = input("\n  > ")
        if (_aux.replace(" ", "") == ""): continue
        while (_aux.replace(" ", "") != ""):  # input termina al ingresar línea vacía (simplemente, tecla enter).
            BUFFER += _aux + "\n"
            _aux = input("... ")

        instructions = BUFFER.split("\n")
        userCMD = instructions[0].replace(" ", "").lower()

        if (userCMD == "connect"):
            if (isConnected):
                print("Oiga, ud. ya se encuentra conectado al servidor. Tranquilícese.")
                continue

            try:
                if (instructions[1].lower() == "quick"):
                    host_IP = "127.0.0.8"; host_port = 6000  # testing only!!
                else:
                    host_IP = instructions[1].split(": ")[1]
                    if (host_IP.lower() == "default"): host_IP = "127.0.0.8"
                    host_port = instructions[2].split(": ")[1]
                    if (host_port.lower() == "default"):
                        host_port = 6000
                    else:
                        host_port = int(host_port)
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((host_IP, host_port))
                isConnected = True
            except Exception as e:
                PrintError("[!] Error: no se pudo conectar al servidor o no siguió la sintaxis adecuada.")
                print("Detalles del error: ", e)

        elif (userCMD == "quit"):
            if (isConnected):
                connection.send(BUFFER.encode(ENCODING))
                connection.close()
                isConnected = False
            exit(0)

        elif (userCMD == "disconnect"):
            if (not isConnected):
                print("Ud. no se encuentra conectado al servidor.")
                continue
            connection.send(BUFFER.encode(ENCODING))
            connection.close()
            PrintInfo("Ud. se ha desconectado del servidor")
            isConnected = False

        elif (userCMD == "help" or userCMD == "ayua"):
            ShowHelp();
            continue

        else:
            if (isConnected):
                connection.send(BUFFER.encode(ENCODING))
            else:
                PrintError(
                    "[!] Error: no está actualmente conectado al servidor. Primero que nada debe ejecutar comando \'connect\'")
        """ en este punto envió el request """

        """ ahora espera la respuesta del servidor... """
        if (isConnected):
            BUFFER = connection.recv(BUFFER_SIZE).decode(ENCODING)
            print("Respuesta recibida del servidor: ", end="")
            PrintInfo("\'%s\'" % BUFFER)


if (__name__ == "__main__"):
    main()
