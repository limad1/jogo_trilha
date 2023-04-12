import socket
import sys
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
while True:
    a = " "
    while a != "\r":
        a = tcp.recv(1).decode("utf-8")
        print(a, end='', flush=True)
    print("")
    msg = input('> ')
    while len(msg)<=0:
        msg = input('> ')
    tcp.send(bytes(msg, 'utf-8'))
tcp.close()