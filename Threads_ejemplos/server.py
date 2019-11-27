# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()


# thread fuction
def threaded(c):
    while True:
        # DEPENDIENDO DE LA INSTRUCCION, EL SERVIDOR DEJARA MOVERSE SIN LOCK (COMO LECTURA DE DATOS)
        
        while (print_lock.locked()):
            continue
        #   ACA RECIBIMOS EL DATO, SI ES UNA INSTRUCCION QUE NECESITA LOCK, LO ACTIVAMOS Y PASAMOS A VER EL RESTO
        data = c.recv(1024)
        while (print_lock.locked()):
            continue
        #   EL DOBLE WHILE NO ES BELLO, PERO ES PARA QUE PASE UN DATO A LA VEZ Y NO SE SOBRECARGUE SOLO EL data

        #   LO DECODIFICAMOS PARA QUE LO PODAMOS USAR BIEN COMO STR
        data = data.decode('utf-8')
        #   SI SE DA UNA CONDICION RANDOM PARA QUE SE HAGA LOCK
        if ("lock" in data):
            try:
                print_lock.acquire()
                print("YES")
            except:
                pass

        if not data:
            print('Bye')
            #   HACEMOS UNA SALIDA GENERICA DEL SERVER
            break
        
        print(data)


        if (print_lock.locked()):
            #   ESTA ES LA CONDICION PARA QUE EL SERVER QUE ESTA EN MODO LOCK, HACIENDO LO QUE SEA, CUANDO ACABE, LIBERE EL LOCK
            #   EN ESTE CASO, ENVIARE UN INPUT CUALQUIERA AL CLIENTE QUE LO ESTA GENERANDO PARA QUE LO TERMINE
            Confirm = "Ready?"
            c.send(Confirm.encode(('utf-8')))
            c.recv(1024)
            print_lock.release()
            print("NO\n")

        #   HAY QUE GENERAR AQUI EL MENSAJE DE RESPUESTA QUE SE ESPERA
        data = "WOW " + data
        #   ENVIAMOS EL MENSAJE DE RESPUESTA
        c.send(data.encode('utf-8'))

        # connection closed

    c.close()
    print("Conexión terminada.")
    return


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("Socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        print("Esperando conexión...")
        c, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


Main()
#if __name__ == '__main__':
#    Main() 