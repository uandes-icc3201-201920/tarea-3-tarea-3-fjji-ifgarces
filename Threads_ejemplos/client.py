# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    message = input("Inserte mensaje: ")
    #message = "FJJI HERE!"
    while True:

        # message sent to server
        s.send(message.encode('utf-8'))

        # message received from server
        data = s.recv(1024)
        data = data.decode('utf-8')
        #la condicion no es robusta, solo es para ejemplificar 
        while ("?" in data):
            print(data)
            message = "A"+input("Presione enter para completar... ")
            s.send(message.encode('utf-8'))
            data = s.recv(1024)
            data = data.decode('utf-8')
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', data)
        print("EL MSG ES ", data)
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            message = input("Inserte msg")
            continue
        else:
            break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main() 