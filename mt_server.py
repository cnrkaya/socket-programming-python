# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

def proccessData(data):
    commandNum = 3
    commands = data.split(" ")
    
    if len(commands) == commandNum :
        return 'ACK'
    else:
        return 'Command size must be {}'.format(commandNum)

# thread fuction
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('No other data, connection will close')

            # lock released on exit
            print_lock.release()
            break

        string_data = str(data.decode('ascii'))

        print('Recieved message: '+string_data )
        reply = proccessData(string_data)

        # send reply to client
        c.send(reply.encode('ascii'))

    # connection closed
    c.close()


def Main():
   # host = '25.48.108.244'
    host = ''
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        conn, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn,))
    s.close()


if __name__ == '__main__':
    Main()